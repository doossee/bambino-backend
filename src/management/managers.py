from django.contrib.auth.models import BaseUserManager


class CustomUserManager(BaseUserManager):
    """Custom User manager"""

    def create_user(self, mobile, password=None, **extra_fields):
        if not mobile:
            raise ValueError("User must have an mobile")
        user = self.model(mobile=mobile, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, mobile, password=None, **extra_fields):
        user = self.create_user(mobile, password=password, **extra_fields)
        user.is_active = True
        user.is_staff = True
        user.is_admin = True
        user.save(using=self._db)
        return user
