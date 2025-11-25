from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, throttling
from backend.api.models import EmailVerification
from backend.api.services.verification import generate_verification, email_verifier
import logging

logger = logging.getLogger(__name__)

# Simple rate throttle (per IP)
class EmailSendRateThrottle(throttling.SimpleRateThrottle):
	"""
	Throttle class to limit email send requests per IP.
	"""
	scope = 'email_send'

	def get_cache_key(self, request, view):
		"""
		Returns a unique cache key for the requesting IP.
		"""
		return self.get_ident(request)

class SendEmailView(APIView):
	"""
	API endpoint to handle email verification requests.
	Throttled per IP. Always responds generically for security.
	"""
	throttle_classes = [EmailSendRateThrottle]

	def post(self, request):
		"""
		Accepts an email, creates or finds a verification object, and triggers email sending.
		"""
		email = request.data.get('email')
		if not email:
			return Response({'detail': 'Email required.'}, status=status.HTTP_400_BAD_REQUEST)
		try:
			# Always respond generically
			obj, created = EmailVerification.objects.get_or_create(email=email)
			if not obj.verified:
				try:
					generate_verification(obj)
				except Exception as e:
					logger.error(f"Error sending verification email for {email}", exc_info=True)
			logger.info(f"Verification requested for {email}")
		except Exception as e:
			logger.error(f"Error processing email verification for {email}", exc_info=True)
		return Response({'detail': 'If the email exists, a verification link was sent.'}, status=status.HTTP_201_CREATED)

class VerifyTokenView(APIView):
	"""
	API endpoint to verify email tokens.
	Accepts a token, verifies it, and updates the email status.
	"""
	def post(self, request):
		"""
		Accepts a token, verifies it, and returns the result.
		"""
		token = request.data.get('token')
		if not token:
			return Response({'detail': 'Token required.'}, status=status.HTTP_400_BAD_REQUEST)
		try:
			success, message = email_verifier(token)
			status_code = status.HTTP_200_OK if success else status.HTTP_400_BAD_REQUEST
		except Exception as e:
			logger.error("Error verifying token", exc_info=True)
			message = "Internal server error."
			status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
		return Response({'detail': message}, status=status_code)
