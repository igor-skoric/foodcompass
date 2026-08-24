from django.test import Client, SimpleTestCase, override_settings

from website.i18n import apply_language_prefix, strip_language_prefix


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
