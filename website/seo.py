from django.conf import settings
from django.urls import translate_url


OG_IMAGE_PATH = '/static/og-default.jpg'
OG_IMAGE_ALT = 'Food Compass — HACCP i digitalizacija HACCP sistema'
OG_IMAGE_WIDTH = 1200
OG_IMAGE_HEIGHT = 630


def _absolute(path):
    if not path:
        return ''
    if path.startswith('http://') or path.startswith('https://'):
        return path
    return settings.SITE_URL.rstrip('/') + path


def page_seo(title, description, *, image=None, og_type='website', published=None, image_alt=None):
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
        'image_alt': image_alt or OG_IMAGE_ALT,
        'og_type': og_type,
        'published': published,
    }


def canonical_url(request):
    path = translate_url(request.path, settings.LANGUAGE_CODE) or request.path
    return settings.SITE_URL.rstrip('/') + path
