from django.db import models
from django.utils.translation import gettext_lazy as _


class OrderStatusChoices(models.TextChoices):
    """
    Order status choices
    """

    PENDING = "pe", _("Pending")
    COMLETED = "de", _("Delivered")
    CANCELLED = "ce", _("Cancelled")


class DeliveryTypeChoices(models.TextChoices):
    """
    Delivery type choices
    """

    SHIPPING = "sh", _("Shipping")
    PICKUP = "pu", _("Pick up")
