from rest_framework import serializers

from .models import User, OTP


class SendOTPSerializer(serializers.Serializer):
    """
    OTP Send serializer
    """

    phone_number = serializers.CharField()


class VerifyOTPSerializer(serializers.Serializer):
    """
    OTP Verify serializer
    """

    phone_number = serializers.CharField()
    otp_code = serializers.CharField()


class ProfileMeta:
    exclude = ["password", "is_staff", "is_superuser"]
    read_only_fields = ["created_at", "updated_at", "last_login", "date_joined"]


class UserSerializer(serializers.ModelSerializer):
    """User model serializer"""

    class Meta(ProfileMeta):
        model = User


class MeUserSerializer(serializers.ModelSerializer):
    """User model serializer"""

    class Meta(ProfileMeta):
        model = User
