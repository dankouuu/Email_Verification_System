# import dependencies
import jwt
import requests
from datetime import datetime, timedelta
from django.conf import settings
from django.utils import timezone
from backend.api.models import EmailVerification
from backend.api.settings_email_verification import JWT_SECRET, JWT_EXPIRY_MINUTES, MAILGUN_API_KEY, MAILGUN_DOMAIN, MAILGUN_FROM_EMAIL
from backend.api.services.tasks import send_verification_email_task
import logging

logger = logging.getLogger(__name__)

def generate_verification(email_obj):
	"""
	Generates a JWT token for email verification and queues an email with the verification link.
	Args:
		email_obj (EmailVerification): The email verification object.
	Returns:
		str: The generated JWT token.
	"""
	payload = {
		'email_id': email_obj.id,
		'exp': datetime.utcnow() + timedelta(minutes=JWT_EXPIRY_MINUTES),
		'type': 'email_verification',
	}
	token = jwt.encode(payload, JWT_SECRET, algorithm='HS256')
	from backend.api.settings_email_verification import FRONTEND_VERIFY_URL
	verification_link = f"{FRONTEND_VERIFY_URL}?token={token}"

	# Send email asynchronously via Celery
	if MAILGUN_API_KEY and MAILGUN_DOMAIN:
		send_verification_email_task.delay(email_obj.id, verification_link)
		logger.info(f"Queued verification email to {email_obj.email}")
	else:
		logger.warning("Mailgun config missing, email not sent.")

	return token

def email_verifier(token):
	"""
	Verifies the JWT token, marks the email as verified if valid.
	Args:
		token (str): The JWT token to verify.
	Returns:
		tuple: (success: bool, message: str)
	"""
	try:
		payload = jwt.decode(token, JWT_SECRET, algorithms=['HS256'])
		if payload.get('type') != 'email_verification':
			logger.warning("Invalid token type.")
			return False, "Invalid token type."
		email_id = payload['email_id']
		email_obj = EmailVerification.objects.get(id=email_id)
		if not email_obj.verified:
			email_obj.verified = True
			email_obj.save()
			logger.info(f"Email {email_obj.email} verified.")
			return True, "Email verified."
		else:
			logger.info(f"Email {email_obj.email} already verified.")
			return True, "Email already verified."
	except jwt.ExpiredSignatureError:
		logger.warning("Token expired.")
		return False, "Token expired."
	except (jwt.InvalidTokenError, EmailVerification.DoesNotExist) as e:
		logger.warning(f"Invalid token or email: {e}")
		return False, "Invalid token."
