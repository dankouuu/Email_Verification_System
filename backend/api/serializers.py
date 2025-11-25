from rest_framework import serializers
from backend.api.models import EmailVerification

class EmailVerificationSerializer(serializers.ModelSerializer):
    """
    Serializer for the EmailVerification model.
    """
    class Meta:
        model = EmailVerification
        fields = ['id', 'email', 'verified', 'created_at', 'updated_at']
