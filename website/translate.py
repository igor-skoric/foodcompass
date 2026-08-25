import json
import logging
import re
import time
import urllib.error
import urllib.parse
import urllib.request

logger = logging.getLogger(__name__)

SOURCE_LANG = 'sr'
TARGET_LANGS = ('en', 'ru')
FIELDS = ('title', 'excerpt', 'body')
CHUNK_SIZE = 1200
REQUEST_TIMEOUT = 20
MAX_TEXT_LENGTH = 80_000
MIN_REQUEST_INTERVAL = 0.25
USER_AGENT = (
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
    'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
)
ENDPOINTS = (
    'https://clients5.google.com/translate_a/t?client=dict-chrome-ex',
    'https://translate.googleapis.com/translate_a/single?client=gtx&dt=t',
)
HTML_CLOSE_RE = re.compile(r'</(?:p|h[1-6]|li|ul|ol|blockquote|div|table)>', re.I)

_last_request_at = 0.0


class TranslationError(Exception):
    pass


def translate_article(title, excerpt, body):
    source = {
        'title': title or '',
        'excerpt': excerpt or '',
        'body': body or '',
    }
    if not any(value.strip() for value in source.values()):
        raise TranslationError('Unesite srpski tekst.')
    total = sum(len(value) for value in source.values())
    if total > MAX_TEXT_LENGTH:
        raise TranslationError('Tekst je predugačak za automatski prevod.')

    result = {}
    for lang in TARGET_LANGS:
        translated = translate_fields(source, lang)
        for field, value in translated.items():
            result[f'{field}_{lang}'] = value
    return result


def fill_empty_translations(article):
    filled = []
    for lang in TARGET_LANGS:
        pending = {}
        for field in FIELDS:
            current = (getattr(article, f'{field}_{lang}') or '').strip()
            source = getattr(article, field) or ''
            if not current and source.strip():
                pending[field] = source
        if not pending:
            continue
        try:
            translated = translate_fields(pending, lang)
        except TranslationError:
            logger.exception('Automatski prevod na %s nije uspeo.', lang)
            continue
        for field, value in translated.items():
            if value and value.strip():
                setattr(article, f'{field}_{lang}', value)
                filled.append(f'{field}_{lang}')
    return filled


def translate_fields(fields, target):
    translated = {}
    for field, value in fields.items():
        if not (value or '').strip():
            translated[field] = ''
            continue
        translated[field] = translate_text(value, target, html=(field == 'body'))
    return translated


def translate_text(text, target, html=False):
    if not (text or '').strip():
        return ''
    parts = _split_html(text) if html else _split_plain(text)
    return ''.join(_google_translate(part, target) for part in parts)


def _split_plain(text):
    if len(text) <= CHUNK_SIZE:
        return [text]
    parts = []
    rest = text
    while rest:
        if len(rest) <= CHUNK_SIZE:
            parts.append(rest)
            break
        cut = rest.rfind(' ', 0, CHUNK_SIZE)
        if cut < CHUNK_SIZE // 3:
            cut = CHUNK_SIZE
        parts.append(rest[:cut])
        rest = rest[cut:]
    return parts


def _split_html(html):
    if len(html) <= CHUNK_SIZE:
        return [html]
    pieces = []
    start = 0
    for match in HTML_CLOSE_RE.finditer(html):
        pieces.append(html[start:match.end()])
        start = match.end()
    if start < len(html):
        pieces.append(html[start:])
    chunks = []
    buf = ''
    for piece in pieces:
        if not piece:
            continue
        if buf and len(buf) + len(piece) > CHUNK_SIZE:
            chunks.append(buf)
            buf = piece
        else:
            buf += piece
    if buf:
        chunks.append(buf)
    out = []
    for chunk in chunks:
        if len(chunk) <= CHUNK_SIZE:
            out.append(chunk)
        else:
            out.extend(_split_plain(chunk))
    return out or [html]


def _google_translate(text, target):
    last_error = None
    for endpoint in ENDPOINTS:
        try:
            return _request_translation(endpoint, text, target)
        except TranslationError as exc:
            last_error = exc
            logger.warning('Translate endpoint failed (%s): %s', endpoint, exc)
    raise last_error or TranslationError('Prevod nije uspeo. Pokušajte ponovo.')


def _request_translation(endpoint, text, target):
    params = urllib.parse.urlencode({
        'sl': SOURCE_LANG,
        'tl': target,
        'q': text,
    })
    request = urllib.request.Request(
        f'{endpoint}&{params}',
        headers={'User-Agent': USER_AGENT},
    )
    payload = None
    for attempt in range(4):
        _throttle()
        try:
            with urllib.request.urlopen(request, timeout=REQUEST_TIMEOUT) as response:
                payload = json.loads(response.read().decode('utf-8'))
            break
        except urllib.error.HTTPError as exc:
            last_error = TranslationError(
                'Servis za prevod trenutno nije dostupan. Pokušajte ponovo.'
            )
            last_error.__cause__ = exc
            if exc.code == 429 and attempt < 3:
                time.sleep(1.2 * (attempt + 1))
                continue
            raise last_error from exc
        except (urllib.error.URLError, TimeoutError, json.JSONDecodeError, UnicodeDecodeError) as exc:
            raise TranslationError(
                'Prevod nije uspeo. Proverite internet vezu i pokušajte ponovo.'
            ) from exc

    translated = _translated_from_payload(payload)
    if not translated.strip():
        raise TranslationError('Prevod je vratio prazan tekst.')
    return translated


def _translated_from_payload(payload):
    if isinstance(payload, str):
        return payload
    if isinstance(payload, list) and payload:
        if isinstance(payload[0], str):
            return ''.join(part for part in payload if isinstance(part, str))
        if isinstance(payload[0], list):
            return ''.join(
                part[0] for part in payload
                if part and isinstance(part[0], str)
            )
    return ''


def _throttle():
    global _last_request_at
    wait = MIN_REQUEST_INTERVAL - (time.monotonic() - _last_request_at)
    if wait > 0:
        time.sleep(wait)
    _last_request_at = time.monotonic()
