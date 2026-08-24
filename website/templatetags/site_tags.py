from django import template
from django.urls import reverse

from website.copy_loader import get_service, site_copy

register = template.Library()


@register.simple_tag(takes_context=True)
def nav_url(context, item):
    if item.get('slug'):
        return reverse(item['url_name'], kwargs={'slug': item['slug']})
    return reverse(item['url_name'])


@register.inclusion_tag('includes/breadcrumbs.html', takes_context=True)
def breadcrumbs(context):
    copy = site_copy()
    request = context['request']
    raw_parts = [p for p in request.path.split('/') if p]
    lang_prefix = ''
    if raw_parts and raw_parts[0] in ('en', 'ru'):
        lang_prefix = f'/{raw_parts[0]}'
        parts = raw_parts[1:]
    else:
        parts = [p for p in raw_parts if p != 'sr']
    crumbs = [{'label': copy.STRINGS['crumb_home'], 'url': reverse('home')}]
    path = ''
    for i, part in enumerate(parts):
        path += f'/{part}'
        is_last = i == len(parts) - 1
        if parts[0] == 'usluge' and i == 1:
            service = get_service(part)
            label = service['title'] if service else part
        elif parts[0] == 'aktuelnosti' and i == 1:
            article = context.get('article')
            label = article.display_title if article else part
        else:
            label = copy.CRUMB_LABELS.get(part, part)
        if is_last:
            crumbs.append({'label': label, 'url': None})
        elif parts[0] == 'aktuelnosti' and i == 0:
            crumbs.append({'label': label, 'url': reverse('news')})
        else:
            crumbs.append({'label': label, 'url': f'{lang_prefix}{path}/'})
    return {'crumbs': crumbs}


@register.filter
def hero_image(name):
    mapping = {
        'about': 'images/page-about.jpg',
        'services': 'images/page-services.jpg',
        'haccp': 'images/page-haccp.jpg',
        'iso': 'images/page-iso.jpg',
        'deklarisanje': 'images/page-deklarisanje.jpg',
        'gap': 'images/page-gap.jpg',
        'digital': 'images/page-digital.jpg',
        'supervision': 'images/page-supervision.jpg',
        'journey': 'images/page-journey.jpg',
        'contact': 'images/page-contact.jpg',
    }
    return mapping.get(name, 'images/page-services.jpg')
