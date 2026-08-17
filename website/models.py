from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils import timezone
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
