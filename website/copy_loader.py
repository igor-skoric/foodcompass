from django.db.models import F
from django.utils import translation

from .models import Article


def lang_code():
    code = (translation.get_language() or 'sr')[:2].lower()
    return code if code in ('sr', 'en', 'ru') else 'sr'


def site_copy():
    code = lang_code()
    if code == 'en':
        from website import copy_en as mod
    elif code == 'ru':
        from website import copy_ru as mod
    else:
        from website import content as mod
    return mod


def get_service(slug):
    return next((item for item in site_copy().SERVICES if item['slug'] == slug), None)


def get_service_cards():
    copy = site_copy()
    cards = []
    for index, service in enumerate(copy.SERVICES, start=1):
        cards.append({
            'number': f'{index:02d}',
            'title': service['title'],
            'standards': service.get('standards') or [],
            'desc': service.get('card') or service['short'],
            'icon': service['icon'],
            'url_name': 'service_detail',
            'slug': service['slug'],
            'flagship': False,
        })
    cards.append({
        'number': '06',
        'title': copy.STRINGS['journey_card_title'],
        'standards': [],
        'desc': copy.STRINGS['journey_card_desc'],
        'icon': 'journey',
        'url_name': 'journey',
        'slug': None,
        'flagship': True,
    })
    return cards


def published_articles():
    return Article.objects.filter(is_published=True).order_by(
        F('published_at').desc(nulls_last=True),
        '-created_at',
    )
