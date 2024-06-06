from django.contrib.auth import views
from rest_framework import viewsets

class MultiSerializerMixin(viewsets.GenericViewSet):
    """
    Mixin that allows use different serializer for different actions
    """

    serializer_action_classes = {}

    def get_serializer_class(self):
        return self.serializer_action_classes.get(self.action, super().get_serializer_class())

class LogoutView(views.LogoutView):
    """ """

    http_method_names = ["get", "post", "options"]

    def get(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)
