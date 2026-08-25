from unittest.mock import patch
from decimal import Decimal
from io import BytesIO

from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client, SimpleTestCase, TestCase, override_settings
from django.utils import timezone
from PIL import Image

from website.i18n import apply_language_prefix, strip_language_prefix
from website.images import COVER_SIZE, ImageProcessingError, constrain_inline_image, normalize_cover
from website.models import Article, Partner
from website.translate import fill_empty_translations, translate_article


class LanguagePrefixTests(SimpleTestCase):
    def test_strip_language_prefix(self):
        self.assertEqual(strip_language_prefix('/en/o-nama/'), '/o-nama/')
        self.assertEqual(strip_language_prefix('/ru/'), '/')
        self.assertEqual(strip_language_prefix('/o-nama/'), '/o-nama/')
        self.assertEqual(strip_language_prefix('/en/o-nama/?x=1'), '/o-nama/?x=1')

    def test_apply_language_prefix(self):
        self.assertEqual(apply_language_prefix('/en/o-nama/', 'ru'), '/ru/o-nama/')
        self.assertEqual(apply_language_prefix('/en/o-nama/', 'sr'), '/o-nama/')
        self.assertEqual(apply_language_prefix('/', 'en'), '/en/')
        self.assertEqual(apply_language_prefix('/en/', 'sr'), '/')


@override_settings(ALLOWED_HOSTS=['127.0.0.1', 'testserver', 'localhost'])
class LanguageSwitchTests(SimpleTestCase):
    def setUp(self):
        self.client = Client(HTTP_HOST='127.0.0.1')

    def _switch(self, language, next_url):
        return self.client.post(
            '/i18n/setlang/',
            {'language': language, 'next': next_url},
            HTTP_HOST='127.0.0.1',
        )

    def test_second_switch_leaves_first_language(self):
        first = self._switch('en', '/')
        self.assertEqual(first.status_code, 302)
        self.assertEqual(first['Location'], '/en/')

        second = self._switch('ru', '/en/')
        self.assertEqual(second.status_code, 302)
        self.assertEqual(second['Location'], '/ru/')

        third = self._switch('sr', '/ru/o-nama/')
        self.assertEqual(third.status_code, 302)
        self.assertEqual(third['Location'], '/o-nama/')


def _fake_google_translate(text, target):
    prefix = 'EN:' if target == 'en' else 'RU:'
    return f'{prefix}{text}'


@override_settings(ALLOWED_HOSTS=['127.0.0.1', 'testserver', 'localhost'])
class ArticleTranslationTests(TestCase):
    def test_translate_article_fills_en_and_ru(self):
        with patch('website.translate._google_translate', side_effect=_fake_google_translate):
            result = translate_article('Naslov', 'Opis', '<p>Tekst</p>')
        self.assertEqual(result['title_en'], 'EN:Naslov')
        self.assertEqual(result['body_ru'], 'RU:<p>Tekst</p>')

    def test_fill_empty_translations_skips_existing(self):
        article = Article(
            title='Naslov',
            excerpt='Opis',
            body='Tekst',
            title_en='Existing',
        )
        with patch('website.translate._google_translate', side_effect=_fake_google_translate):
            filled = fill_empty_translations(article)
        self.assertEqual(article.title_en, 'Existing')
        self.assertEqual(article.excerpt_en, 'EN:Opis')
        self.assertEqual(article.body_ru, 'RU:Tekst')
        self.assertNotIn('title_en', filled)

    def test_translate_endpoint_requires_staff(self):
        client = Client(HTTP_HOST='127.0.0.1')
        response = client.post(
            '/app/aktuelnosti/prevod/',
            data='{"title":"Test"}',
            content_type='application/json',
        )
        self.assertEqual(response.status_code, 302)

    def test_translate_endpoint_returns_json(self):
        User = get_user_model()
        User.objects.create_user('owner', password='secret', is_staff=True)
        client = Client(HTTP_HOST='127.0.0.1')
        client.login(username='owner', password='secret')
        with patch('website.app_views.translate_article', return_value={
            'title_en': 'Title',
            'excerpt_en': '',
            'body_en': '<p>Body</p>',
            'title_ru': 'Заголовок',
            'excerpt_ru': '',
            'body_ru': '<p>Текст</p>',
        }):
            response = client.post(
                '/app/aktuelnosti/prevod/',
                data='{"title":"Naslov","excerpt":"","body":"<p>Tekst</p>"}',
                content_type='application/json',
            )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['title_en'], 'Title')
        self.assertEqual(response.json()['title_ru'], 'Заголовок')

    def test_news_form_has_translate_button(self):
        User = get_user_model()
        User.objects.create_user('owner', password='secret', is_staff=True)
        client = Client(HTTP_HOST='127.0.0.1')
        client.login(username='owner', password='secret')
        response = client.get('/app/aktuelnosti/nova/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Popuni prevod (EN i RU)')
        self.assertContains(response, '/app/aktuelnosti/prevod/')
        self.assertContains(response, '1600 × 900 px')

    def test_saving_article_autofills_blank_translations(self):
        User = get_user_model()
        User.objects.create_user('owner', password='secret', is_staff=True)
        client = Client(HTTP_HOST='127.0.0.1')
        client.login(username='owner', password='secret')
        with patch('website.translate._google_translate', side_effect=_fake_google_translate):
            response = client.post('/app/aktuelnosti/nova/', {
                'title': 'Nova vest',
                'excerpt': 'Kratak opis',
                'body': '<p>Sadržaj</p>',
                'is_published': 'on',
            })
        self.assertEqual(response.status_code, 302)
        article = Article.objects.get(title='Nova vest')
        self.assertEqual(article.title_en, 'EN:Nova vest')
        self.assertEqual(article.title_ru, 'RU:Nova vest')
        self.assertIn('toast=translated', response['Location'])


def _png_file(width, height, name='photo.png'):
    buffer = BytesIO()
    Image.new('RGB', (width, height), (180, 40, 40)).save(buffer, format='PNG')
    return SimpleUploadedFile(name, buffer.getvalue(), content_type='image/png')


class CoverImageTests(SimpleTestCase):
    def test_normalize_cover_makes_16_by_9(self):
        result = normalize_cover(_png_file(400, 900))
        image = Image.open(result)
        self.assertEqual(image.size, COVER_SIZE)
        self.assertEqual(image.format, 'JPEG')

    def test_constrain_inline_image_caps_width(self):
        result = constrain_inline_image(_png_file(2000, 1000, 'wide.png'))
        image = Image.open(result)
        self.assertEqual(image.size, (1600, 800))

    def test_invalid_image_raises(self):
        bogus = SimpleUploadedFile('x.png', b'not-an-image', content_type='image/png')
        with self.assertRaises(ImageProcessingError):
            normalize_cover(bogus)


@override_settings(ALLOWED_HOSTS=['127.0.0.1', 'testserver', 'localhost'])
class PartnerFormTests(TestCase):
    def test_create_partner_without_payments(self):
        User = get_user_model()
        User.objects.create_user('owner', password='secret', is_staff=True)
        client = Client(HTTP_HOST='127.0.0.1')
        client.login(username='owner', password='secret')
        today = timezone.localdate().isoformat()
        response = client.post('/app/klijenti/novi/', {
            'name': 'Nova pekara',
            'recorded_on': today,
            'due_on': today,
            'agreed_amount': '120000.00',
            'status': 'pending',
            'description': '',
            'payments-TOTAL_FORMS': '1',
            'payments-INITIAL_FORMS': '0',
            'payments-MIN_NUM_FORMS': '0',
            'payments-MAX_NUM_FORMS': '40',
            'payments-0-amount': '',
            'payments-0-paid_on': today,
            'payments-0-note': '',
        })
        self.assertEqual(response.status_code, 302)
        partner = Partner.objects.get(name='Nova pekara')
        self.assertEqual(partner.payments.count(), 0)
        self.assertEqual(partner.amount, 0)
        self.assertEqual(partner.agreed_amount, Decimal('120000.00'))
        self.assertEqual(partner.remaining_amount, Decimal('120000.00'))

    def test_create_partner_without_any_amounts(self):
        User = get_user_model()
        User.objects.create_user('owner', password='secret', is_staff=True)
        client = Client(HTTP_HOST='127.0.0.1')
        client.login(username='owner', password='secret')
        today = timezone.localdate().isoformat()
        response = client.post('/app/klijenti/novi/', {
            'name': 'Bez iznosa',
            'recorded_on': today,
            'due_on': today,
            'agreed_amount': '',
            'status': 'pending',
            'description': '',
            'payments-TOTAL_FORMS': '1',
            'payments-INITIAL_FORMS': '0',
            'payments-MIN_NUM_FORMS': '0',
            'payments-MAX_NUM_FORMS': '40',
            'payments-0-amount': '',
            'payments-0-paid_on': today,
            'payments-0-note': '',
        })
        self.assertEqual(response.status_code, 302)
        partner = Partner.objects.get(name='Bez iznosa')
        self.assertEqual(partner.agreed_amount, 0)
        self.assertEqual(partner.amount, 0)
        self.assertEqual(partner.payments.count(), 0)

    def test_payments_reduce_remaining(self):
        User = get_user_model()
        User.objects.create_user('owner', password='secret', is_staff=True)
        client = Client(HTTP_HOST='127.0.0.1')
        client.login(username='owner', password='secret')
        today = timezone.localdate().isoformat()
        response = client.post('/app/klijenti/novi/', {
            'name': 'Pekara rate',
            'recorded_on': today,
            'due_on': today,
            'agreed_amount': '100000',
            'status': 'active',
            'description': '',
            'payments-TOTAL_FORMS': '1',
            'payments-INITIAL_FORMS': '0',
            'payments-MIN_NUM_FORMS': '0',
            'payments-MAX_NUM_FORMS': '40',
            'payments-0-amount': '40000',
            'payments-0-paid_on': today,
            'payments-0-note': '1. rata',
        })
        self.assertEqual(response.status_code, 302)
        partner = Partner.objects.get(name='Pekara rate')
        self.assertEqual(partner.amount, Decimal('40000.00'))
        self.assertEqual(partner.remaining_amount, Decimal('60000.00'))

    def test_client_list_shows_balances_and_row_link(self):
        User = get_user_model()
        User.objects.create_user('owner', password='secret', is_staff=True)
        client = Client(HTTP_HOST='127.0.0.1')
        client.login(username='owner', password='secret')
        partner = Partner.objects.create(
            name='Pekara pregled',
            agreed_amount=Decimal('80000.00'),
            amount=Decimal('20000.00'),
            status='active',
        )
        response = client.get('/app/klijenti/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Dogovoreno')
        self.assertContains(response, 'Dato')
        self.assertContains(response, 'Duguju')
        self.assertContains(response, f'/app/klijenti/{partner.pk}/')
        self.assertContains(response, 'app-row-hit__link')


@override_settings(ALLOWED_HOSTS=['127.0.0.1', 'testserver', 'localhost'])
class AppDeleteTests(TestCase):
    def setUp(self):
        User = get_user_model()
        User.objects.create_user('owner', password='secret', is_staff=True)
        self.client = Client(HTTP_HOST='127.0.0.1')
        self.client.login(username='owner', password='secret')

    def test_delete_partner(self):
        partner = Partner.objects.create(name='Za brisanje', status='pending')
        response = self.client.post(f'/app/klijenti/{partner.pk}/brisanje/')
        self.assertEqual(response.status_code, 302)
        self.assertIn('toast=deleted', response['Location'])
        self.assertFalse(Partner.objects.filter(pk=partner.pk).exists())

    def test_delete_article(self):
        article = Article.objects.create(title='Vest za brisanje', body='<p>Tekst</p>')
        response = self.client.post(f'/app/aktuelnosti/{article.pk}/brisanje/')
        self.assertEqual(response.status_code, 302)
        self.assertIn('toast=deleted', response['Location'])
        self.assertFalse(Article.objects.filter(pk=article.pk).exists())

    def test_delete_requires_post(self):
        partner = Partner.objects.create(name='Ostaje', status='pending')
        response = self.client.get(f'/app/klijenti/{partner.pk}/brisanje/')
        self.assertEqual(response.status_code, 405)
        self.assertTrue(Partner.objects.filter(pk=partner.pk).exists())

    def test_message_detail_has_no_reply_cta(self):
        from website.models import ContactMessage
        message = ContactMessage.objects.create(
            name='Ana',
            email='ana@example.com',
            message='Pozdrav',
        )
        response = self.client.get(f'/app/poruke/{message.pk}/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'ana@example.com')
        self.assertNotContains(response, 'Odgovori emailom')

    def test_partner_list_uses_custom_delete_dialog(self):
        Partner.objects.create(name='Pekara', status='pending')
        response = self.client.get('/app/klijenti/')
        self.assertContains(response, 'data-confirm-dialog')
        self.assertContains(response, 'Obrisati klijenta?')
        self.assertContains(response, 'Odustani')

