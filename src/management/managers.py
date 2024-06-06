from django.contrib.auth.models import BaseUserManager


class CustomUserManager(BaseUserManager):
    """
    Custom User manager
    """

    def create_user(self, phone_number, password=None, **extra_fields):
        if not phone_number:
            raise ValueError("User must have a phone number")
        user = self.model(phone_number=phone_number, **extra_fields)
        if password:
            user.set_password(password)
        else:
            user.set_unusable_password()  # Сделать пароль недоступным
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, password=None, **extra_fields):
        user = self.create_user(phone_number, password=password, **extra_fields)
        user.is_active = True
        user.is_staff = True
        user.is_admin = True
        user.save(using=self._db)
        return user
