from django.conf import settings
from django.utils import translation

from .content import CONTACT
from .copy_loader import lang_code, site_copy
from .i18n import strip_language_prefix
from .seo import alternate_urls, canonical_url, og_locale_for


def site_globals(request):
    copy = site_copy()
    return {
        'nav_items': copy.NAV,
        'contact_info': CONTACT,
        'all_services': copy.SERVICES,
        't': copy.STRINGS,
        'site_name': settings.SITE_NAME,
        'site_url': settings.SITE_URL,
        'canonical_url': canonical_url(request),
        'hreflang_urls': alternate_urls(request),
        'og_locale': og_locale_for(lang_code()),
        'current_language': translation.get_language() or 'sr',
        'available_languages': settings.LANGUAGES,
        'language_neutral_path': strip_language_prefix(request.get_full_path()),
    }
