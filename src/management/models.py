import uuid
import random
from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import AbstractUser

from .managers import CustomUserManager


phone_regex = RegexValidator(regex=r"^\+\d{12}$", message="Wrong  number")


class User(AbstractUser):
    """
    Custom User model
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = None
    username = None

    phone_number = models.CharField(
        validators=[phone_regex], max_length=13, unique=True
    )

    objects = CustomUserManager()

    USERNAME_FIELD = "phone_number"
    REQUIRED_FIELDS = []

    def get_full_name(self):
        return f"{self.first_name} - {self.last_name}"

    def get_short_name(self):
        return self.phone_number

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    def __str__(self):
        return self.first_name


class OTP(models.Model):
    """ "
    OTP(One Time Password) model
    """

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    otp_code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)

    def generate_otp(self):
        self.otp_code = str(random.randint(100000, 999999))
        self.save()

    def is_valid(self):
        # Добавьте логику проверки, например, истек ли срок действия OTP
        # Например, если OTP действует 5 минут
        from datetime import timedelta
        from django.utils import timezone

        return self.created_at + timedelta(minutes=5) > timezone.now()
