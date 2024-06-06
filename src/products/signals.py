from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import Brand
from .utils import process_image


@receiver(pre_save, sender=Brand)
def brand_pre_save(sender, instance, **kwargs):
    if instance.icon:
        processed_icon = process_image(instance.icon)
        if processed_icon:
            instance.icon = processed_icon
