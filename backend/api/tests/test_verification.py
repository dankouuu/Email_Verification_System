from django.urls import reverse
from rest_framework.test import APITestCase
from backend.api.models import EmailVerification
from backend.api.services.verification import generate_verification
import jwt
from backend.api.settings_email_verification import JWT_SECRET

class EmailVerificationTests(APITestCase):
    def test_verify_token_already_verified(self):
        obj = EmailVerification.objects.create(email='alreadyverified@example.com', verified=True)
        token = generate_verification(obj)
        url = reverse('verify_token')
        response = self.client.post(url, {'token': token}, format='json')
        self.assertEqual(response.status_code, 200)
        obj.refresh_from_db()
        self.assertTrue(obj.verified)

    def test_send_email_invalid_format(self):
        url = reverse('send_email')
        response = self.client.post(url, {'email': 'notanemail'}, format='json')
        # Should still return 201 for generic response, but not create object
        self.assertEqual(response.status_code, 201)
        self.assertFalse(EmailVerification.objects.filter(email='notanemail').exists())

    def test_send_email_mailgun_failure(self):
        # Patch the Celery task to raise an exception
        from unittest.mock import patch
        url = reverse('send_email')
        with patch('backend.api.services.tasks.send_verification_email_task.delay') as mock_task:
            mock_task.side_effect = Exception('Mailgun failure')
            response = self.client.post(url, {'email': 'failmailgun@example.com'}, format='json')
            self.assertEqual(response.status_code, 201)
            self.assertTrue(EmailVerification.objects.filter(email='failmailgun@example.com').exists())
    def test_send_email_creates_verification(self):
        url = reverse('send_email')
        response = self.client.post(url, {'email': 'test@example.com'}, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertTrue(EmailVerification.objects.filter(email='test@example.com').exists())

    def test_send_email_is_idempotent(self):
        url = reverse('send_email')
        self.client.post(url, {'email': 'test@example.com'}, format='json')
        response = self.client.post(url, {'email': 'test@example.com'}, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(EmailVerification.objects.filter(email='test@example.com').count(), 1)

    def test_verify_token_success(self):
        obj = EmailVerification.objects.create(email='verifyme@example.com')
        token = generate_verification(obj)
        url = reverse('verify_token')
        response = self.client.post(url, {'token': token}, format='json')
        self.assertEqual(response.status_code, 200)
        obj.refresh_from_db()
        self.assertTrue(obj.verified)

    def test_verify_token_invalid(self):
        url = reverse('verify_token')
        response = self.client.post(url, {'token': 'invalidtoken'}, format='json')
        self.assertEqual(response.status_code, 400)

    def test_verify_token_expired(self):
        obj = EmailVerification.objects.create(email='expired@example.com')
        # Create an expired token
        payload = {'email_id': obj.id, 'exp': 0, 'type': 'email_verification'}
        token = jwt.encode(payload, JWT_SECRET, algorithm='HS256')
        url = reverse('verify_token')
        response = self.client.post(url, {'token': token}, format='json')
        self.assertEqual(response.status_code, 400)
