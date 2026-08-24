from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from .content import SERVICES
from .models import Article


class StaticSitemap(Sitemap):
    changefreq = 'weekly'
    protocol = 'https'
    i18n = True
    alternates = True
    x_default = True

    def items(self):
        return [
            ('home', 1.0, 'weekly'),
            ('services', 0.9, 'weekly'),
            ('journey', 0.8, 'monthly'),
            ('support', 0.8, 'monthly'),
            ('about', 0.7, 'monthly'),
            ('about_me', 0.7, 'monthly'),
            ('news', 0.7, 'weekly'),
            ('contact', 0.6, 'monthly'),
            ('terms', 0.2, 'yearly'),
        ]

    def location(self, item):
        return reverse(item[0])

    def priority(self, item):
        return item[1]

    def changefreq(self, item):
        return item[2]


class ServiceSitemap(Sitemap):
    changefreq = 'monthly'
    priority = 0.85
    protocol = 'https'
    i18n = True
    alternates = True
    x_default = True

    def items(self):
        return SERVICES

    def location(self, item):
        return reverse('service_detail', kwargs={'slug': item['slug']})


class NewsSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.6
    protocol = 'https'

    i18n = True
    alternates = True
    x_default = True

    def items(self):
        return Article.objects.filter(is_published=True)

    def lastmod(self, obj):
        return obj.updated_at or obj.published_at

    def location(self, obj):
        return obj.get_absolute_url()
