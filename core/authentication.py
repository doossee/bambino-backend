from django.contrib.auth.models import AnonymousUser

from rest_framework.authentication import SessionAuthentication


class DevAuthentication(SessionAuthentication):

    def authenticate(self, request):
        """ """
        user = getattr(request._request, "user", None)

        if not user or not user.is_active:
            return None

        self.enforce_csrf(request)

        return self.get_user(user), None

    def get_user(self, user):
        if isinstance(user, AnonymousUser):
            return user
