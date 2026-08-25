from decimal import Decimal

from django.conf import settings
from django.db import models
from django.db.models import Sum
from django.urls import reverse
from django.utils import timezone, translation
from django.utils.text import slugify


class Article(models.Model):
    title = models.CharField('Naslov', max_length=220)
    slug = models.SlugField('Slug', max_length=240, unique=True, blank=True)
    excerpt = models.TextField(
        'Kratak opis',
        blank=True,
        help_text='Prikazuje se na listi aktuelnosti i na početnoj.',
    )
    body = models.TextField(
        'Tekst',
        help_text='Glavni sadržaj vesti. Možete formatirati tekst i ubaciti slike.',
    )
    title_en = models.CharField('Naslov (English)', max_length=220, blank=True)
    excerpt_en = models.TextField('Kratak opis (English)', blank=True)
    body_en = models.TextField('Tekst (English)', blank=True)
    title_ru = models.CharField('Naslov (русский)', max_length=220, blank=True)
    excerpt_ru = models.TextField('Kratak opis (русский)', blank=True)
    body_ru = models.TextField('Tekst (русский)', blank=True)
    cover = models.ImageField(
        'Slika',
        upload_to='aktuelnosti/covers/',
        blank=True,
        help_text='Prikazuje se na listi, na početnoj i u headeru vesti ako nema posebne header slike.',
    )
    header_image = models.ImageField(
        'Slika za header',
        upload_to='aktuelnosti/headers/',
        blank=True,
        help_text='Opciono. Ako je prazno, koristi se slika iznad.',
    )
    is_published = models.BooleanField('Objavljeno', default=True)
    published_at = models.DateTimeField('Datum objave', null=True, blank=True)
    language = models.CharField(
        'Jezik',
        max_length=5,
        choices=settings.LANGUAGES,
        default='sr',
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-published_at', '-created_at']
        verbose_name = 'Aktuelnost'
        verbose_name_plural = 'Aktuelnosti'

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            base = slugify(self.title) or 'clanak'
            slug = base
            n = 2
            while Article.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f'{base}-{n}'
                n += 1
            self.slug = slug
        if self.is_published and self.published_at is None:
            self.published_at = timezone.now()
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('news_detail', kwargs={'slug': self.slug})

    def _localized(self, field):
        lang = (translation.get_language() or 'sr')[:2].lower()
        if lang in ('en', 'ru'):
            value = (getattr(self, f'{field}_{lang}') or '').strip()
            if value:
                return getattr(self, f'{field}_{lang}')
        return getattr(self, field) or ''

    @property
    def display_title(self):
        return self._localized('title')

    @property
    def display_excerpt(self):
        return self._localized('excerpt')

    @property
    def display_body(self):
        return self._localized('body')


class ArticleImage(models.Model):
    article = models.ForeignKey(
        Article,
        related_name='images',
        on_delete=models.CASCADE,
        verbose_name='Članak',
    )
    image = models.ImageField('Slika', upload_to='aktuelnosti/gallery/')
    caption = models.CharField('Opis slike', max_length=220, blank=True)
    sort_order = models.PositiveIntegerField('Redosled', default=0)

    class Meta:
        ordering = ['sort_order', 'id']
        verbose_name = 'Slika članka'
        verbose_name_plural = 'Slike članka'

    def __str__(self):
        return self.caption or f'Slika {self.pk}'


class ContactMessage(models.Model):
    name = models.CharField('Ime i prezime', max_length=160)
    email = models.EmailField('Email')
    phone = models.CharField('Telefon', max_length=40, blank=True)
    message = models.TextField('Poruka')
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField('Pročitano', default=False)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Poruka sa sajta'
        verbose_name_plural = 'Poruke sa sajta'

    def __str__(self):
        return f'{self.name} — {self.email}'


class Partner(models.Model):
    STATUS_ACTIVE = 'active'
    STATUS_PENDING = 'pending'
    STATUS_COMPLETED = 'completed'
    STATUS_PAUSED = 'paused'
    STATUS_LATE = 'late'
    STATUS_CHOICES = [
        (STATUS_ACTIVE, 'Aktivan'),
        (STATUS_PENDING, 'Na čekanju'),
        (STATUS_COMPLETED, 'Završen'),
        (STATUS_PAUSED, 'Pauziran'),
        (STATUS_LATE, 'Kasni sa plaćanjem'),
    ]

    name = models.CharField('Naziv klijenta', max_length=180)
    recorded_on = models.DateField('Datum', default=timezone.localdate, db_index=True)
    due_on = models.DateField('Rok', null=True, blank=True, db_index=True)
    amount = models.DecimalField('Iznos', max_digits=12, decimal_places=2, default=0)
    description = models.TextField('Opis', blank=True)
    status = models.CharField(
        'Status',
        max_length=20,
        choices=STATUS_CHOICES,
        default=STATUS_ACTIVE,
        db_index=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-recorded_on', 'name']
        verbose_name = 'Klijent'
        verbose_name_plural = 'Klijenti'

    def __str__(self):
        return self.name

    @staticmethod
    def format_amount(amount):
        value = f'{(amount or Decimal("0")):,.2f}'
        return value.replace(',', 'X').replace('.', ',').replace('X', '.')

    @property
    def amount_display(self):
        return self.format_amount(self.amount)

    @property
    def is_overdue(self):
        return bool(
            self.due_on
            and self.due_on < timezone.localdate()
            and self.status != self.STATUS_COMPLETED
        )

    def sync_amount(self):
        total = self.payments.aggregate(total=Sum('amount'))['total'] or Decimal('0')
        if self.amount != total:
            type(self).objects.filter(pk=self.pk).update(amount=total, updated_at=timezone.now())
            self.amount = total
        return total

    def apply_overdue(self, save=True):
        if self.status == self.STATUS_COMPLETED or not self.is_overdue:
            return False
        if self.status == self.STATUS_LATE:
            return False
        self.status = self.STATUS_LATE
        if save and self.pk:
            type(self).objects.filter(pk=self.pk).update(
                status=self.STATUS_LATE,
                updated_at=timezone.now(),
            )
        return True

    @classmethod
    def mark_overdue(cls):
        today = timezone.localdate()
        return cls.objects.filter(due_on__lt=today).exclude(
            status__in=(cls.STATUS_COMPLETED, cls.STATUS_LATE),
        ).update(status=cls.STATUS_LATE)


class PartnerPayment(models.Model):
    partner = models.ForeignKey(
        Partner,
        related_name='payments',
        on_delete=models.CASCADE,
        verbose_name='Klijent',
    )
    amount = models.DecimalField('Iznos', max_digits=12, decimal_places=2)
    paid_on = models.DateField('Datum rate', default=timezone.localdate)
    note = models.CharField('Napomena', max_length=180, blank=True)

    class Meta:
        ordering = ['paid_on', 'id']
        verbose_name = 'Rata'
        verbose_name_plural = 'Rate'

    def __str__(self):
        return f'{self.partner.name} — {self.amount_display}'

    @property
    def amount_display(self):
        return Partner.format_amount(self.amount)
