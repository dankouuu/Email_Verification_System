from celery import shared_task
import requests
import logging
from backend.api.models import EmailVerification
from backend.api.settings_email_verification import MAILGUN_API_KEY, MAILGUN_DOMAIN, MAILGUN_FROM_EMAIL

logger = logging.getLogger(__name__)

@shared_task(bind=True, max_retries=3, default_retry_delay=60)
def send_verification_email_task(self, email_id, verification_link):
    """
    Celery task to send a verification email via Mailgun.
    Retries up to 3 times on failure.
    Args:
        email_id (int): The ID of the EmailVerification object.
        verification_link (str): The verification link to send.
    Returns:
        int: The HTTP status code from Mailgun API.
    """
    try:
        email_obj = EmailVerification.objects.get(id=email_id)
        response = requests.post(
            f"https://api.mailgun.net/v3/{MAILGUN_DOMAIN}/messages",
            auth=("api", MAILGUN_API_KEY),
            data={
                "from": MAILGUN_FROM_EMAIL,
                "to": [email_obj.email],
                "subject": "Verify your email",
                "text": f"Click the link to verify your email: {verification_link}",
            },
        )
        logger.info(f"Sent verification email to {email_obj.email}, status: {response.status_code}")
        return response.status_code
    except Exception as exc:
        logger.error(f"Failed to send verification email to id={email_id}", exc_info=True)
        raise self.retry(exc=exc)
