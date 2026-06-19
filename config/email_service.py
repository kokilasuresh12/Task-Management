import json
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured


BREVO_EMAIL_URL = 'https://api.brevo.com/v3/smtp/email'


class EmailDeliveryError(Exception):
    pass


def send_brevo_email(*, subject, message, recipient_email, recipient_name=''):
    api_key = settings.BREVO_API_KEY
    sender_email = settings.BREVO_SENDER_EMAIL

    if not api_key:
        raise ImproperlyConfigured('BREVO_API_KEY is not configured.')
    if not sender_email:
        raise ImproperlyConfigured('BREVO_SENDER_EMAIL is not configured.')

    recipient = {'email': recipient_email}
    if recipient_name:
        recipient['name'] = recipient_name

    payload = {
        'sender': {
            'email': sender_email,
            'name': settings.BREVO_SENDER_NAME,
        },
        'to': [recipient],
        'subject': subject,
        'textContent': message,
    }
    request = Request(
        BREVO_EMAIL_URL,
        data=json.dumps(payload).encode('utf-8'),
        headers={
            'accept': 'application/json',
            'api-key': api_key,
            'content-type': 'application/json',
        },
        method='POST',
    )

    try:
        with urlopen(request, timeout=settings.BREVO_TIMEOUT) as response:
            if response.status not in (200, 201, 202):
                raise EmailDeliveryError(
                    f'Brevo returned unexpected status {response.status}.'
                )
    except HTTPError as error:
        try:
            response_body = error.read().decode('utf-8')
            detail = json.loads(response_body).get('message', response_body)
        except (UnicodeDecodeError, json.JSONDecodeError):
            detail = error.reason
        raise EmailDeliveryError(
            f'Brevo rejected the email ({error.code}): {detail}'
        ) from error
    except URLError as error:
        raise EmailDeliveryError(
            f'Could not connect to Brevo: {error.reason}'
        ) from error

