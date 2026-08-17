from django.conf import settings
from django.utils import translation
from .content import CONTACT, NAV, SERVICES


def site_globals(request):
    return {
        'nav_items': NAV,
        'contact_info': CONTACT,
        'all_services': SERVICES,
        'site_name': settings.SITE_NAME,
        'site_url': settings.SITE_URL,
        'current_language': translation.get_language() or 'sr',
        'available_languages': settings.LANGUAGES,
    }
