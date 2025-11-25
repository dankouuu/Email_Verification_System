
from django.db import models

# Email verification model

class EmailVerification(models.Model):
	"""
	Model to store email verification state and timestamps.
	"""
	email = models.EmailField(unique=True)
	verified = models.BooleanField(default=False, db_index=True)
	verification_sent_at = models.DateTimeField(null=True, blank=True)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	def __str__(self):
		"""
		String representation of the email verification object.
		"""
		return f"{self.email} ({'verified' if self.verified else 'not verified'})"
