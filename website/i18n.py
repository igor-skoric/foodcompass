from urllib.parse import urlsplit, urlunsplit

from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect
from django.utils.http import url_has_allowed_host_and_scheme
from django.utils.translation import check_for_language
from django.views.i18n import LANGUAGE_QUERY_PARAMETER


def strip_language_prefix(url):
    """Remove /en, /ru, /sr prefixes so the path can be resolved in the default language."""
    if not url:
        return url
    parsed = urlsplit(url)
    path = parsed.path or '/'
    for code, _name in settings.LANGUAGES:
        prefix = f'/{code}'
        if path == prefix or path.startswith(prefix + '/'):
            path = path[len(prefix):] or '/'
            break
    if not path.startswith('/'):
        path = '/' + path
    return urlunsplit((parsed.scheme, parsed.netloc, path, parsed.query, parsed.fragment))


def apply_language_prefix(url, lang_code):
    """Rewrite a public URL to the chosen language. Default language has no prefix."""
    url = strip_language_prefix(url or '/')
    parsed = urlsplit(url)
    path = parsed.path or '/'
    default = (settings.LANGUAGE_CODE or 'sr')[:2]
    code = (lang_code or default)[:2]
    if code != default:
        path = f'/{code}/' if path == '/' else f'/{code}{path}'
    return urlunsplit((parsed.scheme, parsed.netloc, path, parsed.query, parsed.fragment))


def set_language(request):
    """
    Like Django's set_language, but rewrites /en and /ru prefixes itself.

    LocaleMiddleware forces LANGUAGE_CODE on /i18n/setlang/ because that URL
    has no language prefix (prefix_default_language=False). Django's
    translate_url then cannot resolve a next URL that already starts with
    /en/ or /ru/, so the second language switch would keep the first prefix.
    """
    next_url = request.POST.get('next', request.GET.get('next'))
    if (
        next_url or request.accepts('text/html')
    ) and not url_has_allowed_host_and_scheme(
        url=next_url,
        allowed_hosts={request.get_host()},
        require_https=request.is_secure(),
    ):
        next_url = request.META.get('HTTP_REFERER')
        if not url_has_allowed_host_and_scheme(
            url=next_url,
            allowed_hosts={request.get_host()},
            require_https=request.is_secure(),
        ):
            next_url = '/'

    lang_code = request.POST.get(LANGUAGE_QUERY_PARAMETER) if request.method == 'POST' else None
    if request.method == 'POST' and lang_code and check_for_language(lang_code) and next_url:
        next_url = apply_language_prefix(next_url, lang_code)

    response = HttpResponseRedirect(next_url) if next_url else HttpResponse(status=204)
    if request.method == 'POST' and lang_code and check_for_language(lang_code):
        response.set_cookie(
            settings.LANGUAGE_COOKIE_NAME,
            lang_code,
            max_age=settings.LANGUAGE_COOKIE_AGE,
            path=settings.LANGUAGE_COOKIE_PATH,
            domain=settings.LANGUAGE_COOKIE_DOMAIN,
            secure=settings.LANGUAGE_COOKIE_SECURE,
            httponly=settings.LANGUAGE_COOKIE_HTTPONLY,
            samesite=settings.LANGUAGE_COOKIE_SAMESITE,
        )
    return response
