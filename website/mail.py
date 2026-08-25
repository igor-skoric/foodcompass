import logging

from email.mime.image import MIMEImage
from pathlib import Path

from django.conf import settings
from django.contrib.staticfiles import finders
from django.core.mail import EmailMessage, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils import timezone
from django.utils.html import strip_tags

from .content import CONTACT
from .copy_loader import lang_code, site_copy
from .i18n import apply_language_prefix

logger = logging.getLogger(__name__)

LOGO_STATIC = 'icons/email-compass.png'


def _first_name(full_name):
    parts = (full_name or '').strip().split()
    return parts[0] if parts else ''


def _preview(text, limit=280):
    cleaned = ' '.join((text or '').split())
    if len(cleaned) <= limit:
        return cleaned
    return cleaned[: limit - 1].rsplit(' ', 1)[0] + '…'


def _site_url(path='/'):
    base = settings.SITE_URL.rstrip('/')
    path = path if path.startswith('/') else f'/{path}'
    return apply_language_prefix(f'{base}{path}', lang_code())


def send_contact_message(message):
    phone = message.phone.strip() if message.phone else '—'
    body = (
        f'Nova poruka sa foodcompass.rs\n'
        f'\n'
        f'Ime: {message.name}\n'
        f'Email: {message.email}\n'
        f'Telefon: {phone}\n'
        f'\n'
        f'Poruka:\n{message.message}\n'
    )
    email = EmailMessage(
        subject=f'Upit sa sajta — {message.name}',
        body=body,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=settings.CONTACT_EMAIL,
        reply_to=[message.email],
    )
    sent = email.send(fail_silently=False)
    logger.info('Contact email sent to %s (%s)', settings.CONTACT_EMAIL, sent)
    return sent


def receipt_context(name='', message_text='', logo_url=None):
    copy = site_copy().CONTACT_RECEIPT
    first = _first_name(name)
    return {
        'copy': copy,
        'title': copy['title'].format(name=first) if first else copy['title_plain'],
        'lang': lang_code(),
        'contact': CONTACT,
        'home_url': _site_url('/'),
        'logo_url': logo_url or f'/static/{LOGO_STATIC}',
        'message_preview': _preview(message_text),
        'year': timezone.now().year,
    }


def receipt_html(message=None):
    if message is None:
        context = receipt_context(
            name='Igor Petrović',
            message_text=(
                'Zanima nas HACCP za pogon slatkiša i deklarisanje nove linije proizvoda.'
            ),
        )
    else:
        context = receipt_context(message.name, message.message)
    return render_to_string('emails/contact_receipt.html', context)


def send_contact_receipt(message):
    copy = site_copy().CONTACT_RECEIPT
    context = receipt_context(
        message.name,
        message.message,
        logo_url='cid:foodcompass-logo',
    )
    html = render_to_string('emails/contact_receipt.html', context)
    text = render_to_string('emails/contact_receipt.txt', context).strip() or strip_tags(html)
    email = EmailMultiAlternatives(
        subject=copy['subject'],
        body=text,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[message.email],
        reply_to=[CONTACT['email']],
        headers={
            'Auto-Submitted': 'auto-replied',
            'X-Auto-Response-Suppress': 'All',
            'Precedence': 'auto_reply',
        },
    )
    email.attach_alternative(html, 'text/html')
    email.mixed_subtype = 'related'
    logo_path = finders.find(LOGO_STATIC)
    if logo_path:
        image = MIMEImage(Path(logo_path).read_bytes(), _subtype='png')
        image.add_header('Content-ID', '<foodcompass-logo>')
        image.add_header('Content-Disposition', 'inline', filename='compass.png')
        email.attach(image)
    sent = email.send(fail_silently=False)
    logger.info('Contact receipt sent to %s (%s)', message.email, sent)
    return sent
