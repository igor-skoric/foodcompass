from django.conf import settings
from django.urls import translate_url
from django.utils import translation


OG_IMAGE_PATH = '/static/og-default.jpg'
OG_IMAGE_WIDTH = 1200
OG_IMAGE_HEIGHT = 630

OG_LOCALES = {
    'sr': 'sr_RS',
    'en': 'en_US',
    'ru': 'ru_RU',
}


def og_locale_for(code):
    return OG_LOCALES.get((code or 'sr')[:2], 'sr_RS')


def _absolute(path):
    if not path:
        return ''
    if path.startswith('http://') or path.startswith('https://'):
        return path
    return settings.SITE_URL.rstrip('/') + path


def page_seo(title, description, *, image=None, og_type='website', published=None, image_alt=None):
    from .copy_loader import site_copy

    strings = site_copy().STRINGS
    title = (title or 'Food Compass').strip()
    if 'Food Compass' not in title:
        title = f'{title} | Food Compass'
    image_url = _absolute(image or f'{OG_IMAGE_PATH}?v=5')
    if published and hasattr(published, 'isoformat'):
        published = published.isoformat()
    return {
        'title': title,
        'description': description,
        'image': image_url,
        'image_alt': image_alt or strings['og_image_alt'],
        'og_type': og_type,
        'published': published,
    }


def canonical_url(request):
    lang = translation.get_language() or settings.LANGUAGE_CODE
    path = translate_url(request.path, lang) or request.path
    return settings.SITE_URL.rstrip('/') + path


def alternate_urls(request):
    urls = {}
    for code, _name in settings.LANGUAGES:
        path = translate_url(request.path, code) or request.path
        urls[code] = settings.SITE_URL.rstrip('/') + path
    return urls
