import logging
import re
import shutil
from pathlib import Path

from PIL import Image

from django.conf import settings
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.staticfiles import finders
from django.core.files.storage import default_storage
from django.core.mail import BadHeaderError
from django.core.paginator import Paginator
from django.db.models import F
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.cache import never_cache
from django.views.decorators.http import require_POST
from smtplib import SMTPException

from .content import (
    ABOUT,
    ABOUT_ME,
    CONTACT,
    JOURNEY,
    SEO_PAGES,
    SERVICES,
    SUPPORT,
    TERMS,
    get_service,
    get_service_cards,
)
from .forms import ContactForm
from .mail import send_contact_message
from .models import Article

logger = logging.getLogger(__name__)

HERO_FILE = re.compile(r'^hero(\d+)\.(png|jpe?g)$', re.I)


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
    data = dict(SEO_PAGES.get(key, SEO_PAGES['home']))
    if extra:
        data.update(extra)
    return data


def home(request):
    latest = (
        Article.objects.filter(is_published=True)
        .order_by(F('published_at').desc(nulls_last=True), '-created_at')[:3]
    )
    return render(request, 'pages/home.html', {
        'is_home': True,
        'services': SERVICES,
        'journey': JOURNEY,
        'support': SUPPORT,
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
        'about': ABOUT,
        'seo': _seo('about'),
    })


def about_me(request):
    return render(request, 'pages/about_me.html', {
        'about_me': ABOUT_ME,
        'about_photo': _about_photo(),
        'seo': _seo('about_me'),
    })


def services(request):
    return render(request, 'pages/services.html', {
        'service_cards': get_service_cards(),
        'seo': _seo('services'),
    })


def service_detail(request, slug):
    service = get_service(slug)
    if not service:
        return redirect('services')
    return render(request, 'pages/service_detail.html', {
        'service': service,
        'seo': _seo('services', {
            'title': service['title'],
            'description': service.get('intro') or service['short'],
        }),
        'hero': {
            'image': service.get('hero', 'services'),
            'eyebrow': 'Naše usluge',
            'title': service['title'],
            'subtitle': service.get('short') if service.get('short') and service['short'] != service.get('intro') else '',
            'lead': service.get('intro', ''),
        },
    })


def journey(request):
    return render(request, 'pages/journey.html', {
        'journey': JOURNEY,
        'seo': _seo('journey'),
        'hero': {
            'image': 'journey',
            'eyebrow': 'Od ideje do police',
            'title': 'Od ideje do police',
            'lead': 'Kompletna stručna podrška za razvoj i plasman prehrambenog proizvoda.',
        },
    })


def support(request):
    return render(request, 'pages/support.html', {
        'support': SUPPORT,
        'seo': _seo('support'),
        'hero': {
            'image': 'supervision',
            'eyebrow': 'Stručna podrška',
            'title': SUPPORT['title'],
        },
    })


def news_list(request):
    articles = (
        Article.objects.filter(is_published=True)
        .order_by(F('published_at').desc(nulls_last=True), '-created_at')
    )
    paginator = Paginator(articles, 9)
    page_obj = paginator.get_page(request.GET.get('page'))
    page_numbers = page_obj.paginator.get_elided_page_range(
        page_obj.number, on_each_side=1, on_ends=1
    )
    return render(request, 'news/list.html', {
        'articles': page_obj,
        'page_obj': page_obj,
        'page_numbers': page_numbers,
        'seo': _seo('news'),
    })


def news_detail(request, slug):
    article = get_object_or_404(
        Article.objects.prefetch_related('images'),
        slug=slug,
        is_published=True,
    )
    cover = article.header_image or article.cover
    return render(request, 'news/detail.html', {
        'article': article,
        'seo': {
            'title': article.title,
            'description': article.excerpt or article.title,
        },
        'hero': {
            'image': 'services',
            'cover': cover.url if cover else '',
            'eyebrow': 'Aktuelnosti',
            'title': article.title,
            'lead': article.excerpt or '',
        },
    })


def contact(request):
    sent = False
    send_error = False
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            message = form.save()
            try:
                send_contact_message(message)
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
        'seo': _seo('contact'),
    })


def terms(request):
    return render(request, 'pages/terms.html', {
        'terms': TERMS,
        'seo': _seo('terms'),
    })


@staff_member_required
@require_POST
def upload_image(request):
    uploaded = request.FILES.get('file')
    if not uploaded:
        return JsonResponse({'error': 'Nije poslata slika.'}, status=400)
    path = default_storage.save(f'aktuelnosti/inline/{uploaded.name}', uploaded)
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
