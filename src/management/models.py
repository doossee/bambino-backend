import uuid
from django.db import models
from django.core.validators import RegexValidator

from django.contrib.auth.models import AbstractUser
from .managers import CustomUserManager


phone_regex = RegexValidator(
    regex=r'^\+\d{12}$', message='Wrong  number'
)

class CustomUser(AbstractUser):

    """Custom User model"""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = None
    username = None

    mobile = models.CharField(validators=[phone_regex], max_length=13, unique=True)
    mobile_verified = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'mobile'
    REQUIRED_FIELDS = []

    def get_full_name(self):
        return f"{self.first_name} - {self.last_name}"

    def get_short_name(self):
        return self.mobile

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    def __str__(self):
        return self.first_name