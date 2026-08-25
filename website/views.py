import logging
import re
import shutil
from pathlib import Path

from PIL import Image

from django.conf import settings
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.staticfiles import finders
from django.core.cache import cache
from django.core.files.storage import default_storage
from django.core.mail import BadHeaderError
from django.core.paginator import Paginator
from django.http import Http404, HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.cache import never_cache
from django.views.decorators.http import require_POST
from smtplib import SMTPException

from .content import CONTACT
from .copy_loader import get_service, get_service_cards, published_articles, site_copy
from .forms import ContactForm
from .images import ImageProcessingError, constrain_inline_image
from .mail import receipt_html, send_contact_message, send_contact_receipt
from .models import Article
from .seo import page_seo

logger = logging.getLogger(__name__)

HERO_FILE = re.compile(r'^hero(\d+)\.(png|jpe?g)$', re.I)

# Light contact-form throttle: locmem is per-process (fine for a single Gunicorn worker).
CONTACT_RATE_MAX = 8
CONTACT_RATE_SECONDS = 10 * 60


def _client_ip(request):
    # Reverse proxy (Nginx/Caddy) MUST overwrite X-Forwarded-For — do not append a
    # client-supplied value; the leftmost hop is spoofable. With overwrite there is
    # one trusted IP. If the proxy appends, the rightmost hop is the nearest address
    # Gunicorn should trust. REMOTE_ADDR is the TCP peer (often the proxy itself).
    forwarded = (request.META.get('HTTP_X_FORWARDED_FOR') or '').strip()
    if forwarded:
        return forwarded.split(',')[-1].strip() or 'unknown'
    return (request.META.get('REMOTE_ADDR') or '').strip() or 'unknown'


def _contact_submit_limited(request):
    key = f'contact-form:{_client_ip(request)}'
    if cache.add(key, 1, CONTACT_RATE_SECONDS):
        return False
    try:
        count = cache.incr(key)
    except ValueError:
        cache.set(key, 1, CONTACT_RATE_SECONDS)
        return False
    return count > CONTACT_RATE_MAX


def _export_hero_variants(src: Path):
    image = Image.open(src)
    if image.mode not in ('RGB', 'L'):
        image = image.convert('RGB')
    webp = src.with_suffix('.webp')
    avif = src.with_suffix('.avif')
    source_mtime = src.stat().st_mtime
    if not webp.exists() or webp.stat().st_mtime < source_mtime:
        image.save(webp, 'WEBP', quality=88, method=6)
    if not avif.exists() or avif.stat().st_mtime < source_mtime:
        image.save(avif, 'AVIF', quality=82)


def get_hero_slides():
    dest = Path(settings.BASE_DIR) / 'static' / 'images'
    dest.mkdir(parents=True, exist_ok=True)
    root = Path(settings.BASE_DIR)

    root_heroes = {
        path.name: path
        for path in root.iterdir()
        if path.is_file() and HERO_FILE.match(path.name)
    }

    if root_heroes:
        for name, path in root_heroes.items():
            target = dest / name
            if not target.exists() or path.stat().st_mtime > target.stat().st_mtime:
                shutil.copy2(path, target)
        keep = set(root_heroes)
        for path in list(dest.iterdir()):
            match = HERO_FILE.match(path.name)
            if match and path.name not in keep:
                for extra in (path, path.with_suffix('.webp'), path.with_suffix('.avif')):
                    extra.unlink(missing_ok=True)

    slides = []
    for path in dest.iterdir():
        match = HERO_FILE.match(path.name)
        if not match:
            continue
        _export_hero_variants(path)
        webp = path.with_suffix('.webp')
        avif = path.with_suffix('.avif')
        with Image.open(path) as image:
            width, height = image.size
        slides.append((
            int(match.group(1)),
            {
                'src': f'images/{path.name}',
                'webp': f'images/{webp.name}' if webp.exists() else '',
                'avif': f'images/{avif.name}' if avif.exists() else '',
                'width': width,
                'height': height,
                'version': int(path.stat().st_mtime),
            },
        ))
    slides.sort()
    if slides:
        return [item for _, item in slides]
    fallback = dest / 'hero2.png'
    version = int(fallback.stat().st_mtime) if fallback.exists() else 1
    return [{'src': 'images/hero2.png', 'webp': '', 'avif': '', 'width': 1920, 'height': 1080, 'version': version}]


def _seo(key, extra=None):
    pages = site_copy().SEO_PAGES
    data = dict(pages.get(key, pages['home']))
    if extra:
        data.update(extra)
    published = data.get('published')
    if published and hasattr(published, 'isoformat'):
        published = published.isoformat()
    return page_seo(
        data.get('title'),
        data.get('description'),
        image=data.get('image'),
        og_type=data.get('og_type', 'website'),
        published=published,
        image_alt=data.get('image_alt'),
    )


def home(request):
    copy = site_copy()
    latest = published_articles()[:3]
    return render(request, 'pages/home.html', {
        'is_home': True,
        'home': copy.HOME,
        'services': copy.SERVICES,
        'journey': copy.JOURNEY,
        'support': copy.SUPPORT,
        'latest_news': latest,
        'hero_slides': get_hero_slides(),
        'seo': _seo('home'),
    })


def _about_photo():
    images_dir = Path(settings.BASE_DIR) / 'static' / 'images'
    for name in (
        'about-me.png',
        'about-me.jpg',
        'about-me.jpeg',
        'about-me.webp',
        'sandra_djukanovic_kojic.png',
        'sandra_djukanovic_kojic.jpg',
    ):
        if (images_dir / name).exists():
            return f'images/{name}'
    return ''


def about(request):
    return render(request, 'pages/about.html', {
        'about': site_copy().ABOUT,
        'seo': _seo('about'),
    })


def about_me(request):
    return render(request, 'pages/about_me.html', {
        'about_me': site_copy().ABOUT_ME,
        'about_photo': _about_photo(),
        'seo': _seo('about_me'),
    })


def services(request):
    copy = site_copy()
    return render(request, 'pages/services.html', {
        'service_cards': get_service_cards(),
        'services_page': copy.SERVICES_PAGE,
        'seo': _seo('services'),
    })


def service_detail(request, slug):
    copy = site_copy()
    service = get_service(slug)
    if not service:
        return redirect('services')
    meta = copy.SERVICE_SEO.get(slug, {})
    ui = copy.SERVICE_PAGE
    return render(request, 'pages/service_detail.html', {
        'service': service,
        'service_page': ui,
        'seo': _seo('services', {
            'title': service['title'],
            'description': meta.get('description') or service.get('intro') or service['short'],
        }),
        'hero': {
            'image': service.get('hero', 'services'),
            'eyebrow': ui['eyebrow'],
            'title': service['title'],
            'subtitle': service.get('short') if service.get('short') and service['short'] != service.get('intro') else '',
            'lead': service.get('intro', ''),
        },
    })


def journey(request):
    copy = site_copy()
    page = copy.JOURNEY_PAGE
    return render(request, 'pages/journey.html', {
        'journey': copy.JOURNEY,
        'journey_page': page,
        'seo': _seo('journey'),
        'hero': {
            'image': 'journey',
            'eyebrow': page['hero_eyebrow'],
            'title': page['hero_title'],
            'lead': page['hero_lead'],
        },
    })


def support(request):
    copy = site_copy()
    return render(request, 'pages/support.html', {
        'support': copy.SUPPORT,
        'seo': _seo('support'),
        'hero': {
            'image': 'supervision',
            'eyebrow': copy.SUPPORT['eyebrow'],
            'title': copy.SUPPORT['title'],
        },
    })


def news_list(request):
    articles = published_articles()
    paginator = Paginator(articles, 9)
    page_obj = paginator.get_page(request.GET.get('page'))
    page_numbers = page_obj.paginator.get_elided_page_range(
        page_obj.number, on_each_side=1, on_ends=1
    )
    return render(request, 'news/list.html', {
        'articles': page_obj,
        'page_obj': page_obj,
        'page_numbers': page_numbers,
        'news_page': site_copy().NEWS_PAGE,
        'seo': _seo('news'),
    })


def news_detail(request, slug):
    article = get_object_or_404(
        Article.objects.prefetch_related('images'),
        slug=slug,
        is_published=True,
    )
    cover = article.header_image or article.cover
    news_page = site_copy().NEWS_PAGE
    return render(request, 'news/detail.html', {
        'article': article,
        'news_page': news_page,
        'seo': page_seo(
            article.display_title,
            article.display_excerpt or article.display_title,
            image=cover.url if cover else None,
            og_type='article',
            published=article.published_at,
        ),
        'hero': {
            'image': 'services',
            'cover': cover.url if cover else '',
            'variant': 'article',
            'eyebrow': news_page['eyebrow'],
            'title': article.display_title,
            'lead': article.display_excerpt or '',
        },
    })


def contact(request):
    copy = site_copy()
    sent = False
    send_error = False
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if _contact_submit_limited(request):
            form.add_error(None, copy.CONTACT_PAGE['form_rate_error'])
        elif form.is_valid():
            message = form.save()
            try:
                send_contact_message(message)
                try:
                    send_contact_receipt(message)
                except (SMTPException, BadHeaderError, OSError):
                    logger.exception('Failed to send contact receipt to %s', message.email)
                sent = True
                form = ContactForm()
            except (SMTPException, BadHeaderError, OSError):
                logger.exception('Failed to send contact form email')
                send_error = True
    else:
        form = ContactForm()
    return render(request, 'pages/contact.html', {
        'form': form,
        'sent': sent,
        'send_error': send_error,
        'contact': CONTACT,
        'contact_page': copy.CONTACT_PAGE,
        'seo': _seo('contact'),
    })


def contact_receipt_preview(request):
    if not settings.DEBUG:
        raise Http404()
    return _contact_receipt_preview(request)


@staff_member_required
def _contact_receipt_preview(request):
    return HttpResponse(receipt_html())


def terms(request):
    return render(request, 'pages/terms.html', {
        'terms': site_copy().TERMS,
        'seo': _seo('terms'),
    })


@staff_member_required
@require_POST
def upload_image(request):
    uploaded = request.FILES.get('file')
    if not uploaded:
        return JsonResponse({'error': 'Nije poslata slika.'}, status=400)
    try:
        stored = constrain_inline_image(uploaded)
    except ImageProcessingError as exc:
        return JsonResponse({'error': str(exc)}, status=400)
    path = default_storage.save(f'aktuelnosti/inline/{stored.name}', stored)
    return JsonResponse({'location': f'{settings.MEDIA_URL}{path}'})


@never_cache
def service_worker(request):
    path = finders.find('js/sw.js')
    if not path:
        return HttpResponse('Not found', status=404, content_type='text/plain')
    response = HttpResponse(
        Path(path).read_text(encoding='utf-8'),
        content_type='application/javascript; charset=utf-8',
    )
    response['Service-Worker-Allowed'] = '/'
    response['Cache-Control'] = 'no-cache'
    return response


def robots_txt(request):
    sitemap = settings.SITE_URL.rstrip('/') + '/sitemap.xml'
    body = '\n'.join([
        'User-agent: *',
        'Allow: /',
        'Disallow: /admin/',
        'Disallow: /app/',
        'Disallow: /prijava/',
        'Disallow: /odjava/',
        'Disallow: /media-upload/',
        f'Sitemap: {sitemap}',
        '',
    ])
    return HttpResponse(body, content_type='text/plain')
