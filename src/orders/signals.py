from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Order
from .choices import OrderStatusChoices


@receiver(post_save, sender=Order)
def brand_post_save(sender, created, instance, **kwargs):
    if not created and instance.status == OrderStatusChoices.CANCELLED:
        for order_item in instance.items.all():
            product = order_item.product
            product.balance += order_item.quantity
            product.save()
