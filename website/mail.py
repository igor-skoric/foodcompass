import logging

from django.conf import settings
from django.core.mail import EmailMessage

logger = logging.getLogger(__name__)


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
