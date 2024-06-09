from rest_framework import viewsets, permissions

from .models import Order
from .serializers import OrderSerializer
from .permissions import IsOwnerOrAuthenticated


class OrderViewSet(viewsets.ModelViewSet):
    """
    Order view
    """

    queryset = Order.objects.all()
    pagination_class = None
    serializer_class = OrderSerializer
    # permission_classes = [IsOwnerOrAuthenticated]

    def get_queryset(self):
        qs = (
            super()
            .get_queryset()
            .filter(user=self.request.user.id)
            .prefetch_related("items")
        )
        return qs
