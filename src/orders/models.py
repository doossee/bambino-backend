from django.db import models
from django.core.validators import MinValueValidator
from django.utils.translation import gettext_lazy as _

from src.models import TimeStampedModel
from src.management.models import User
from src.products.models import Product

from .choices import OrderStatusChoices, DeliveryTypeChoices


class Order(TimeStampedModel):
    """
    Order Model
    """

    user = models.ForeignKey(
        verbose_name=_("User"), to=User, related_name="orders", on_delete=models.CASCADE
    )
    status = models.CharField(
        max_length=2,
        choices=OrderStatusChoices.choices,
        default=OrderStatusChoices.PENDING,
    )
    amount = models.PositiveIntegerField(default=0)

    street = models.CharField(max_length=255)
    building_number = models.PositiveSmallIntegerField(
        blank=True, null=True, validators=[MinValueValidator(1)]
    )
    apartment_number = models.PositiveSmallIntegerField(
        blank=True, null=True, validators=[MinValueValidator(1)]
    )
    latitude = models.DecimalField(
        max_digits=22, decimal_places=16, blank=True, null=True
    )
    longtitude = models.DecimalField(
        max_digits=22, decimal_places=16, blank=True, null=True
    )

    delivery_type = models.CharField(
        max_length=2,
        choices=DeliveryTypeChoices.choices,
        default=DeliveryTypeChoices.SHIPPING,
    )
    delivery_date = models.DateTimeField(verbose_name=_("Delivery date and time"))

    class Meta:
        verbose_name = "Order"
        verbose_name_plural = "Orders"

    def __str__(self):
        return f"{self.user}-{self.status}"


class OrderItem(models.Model):
    """
    Order item model
    """

    order = models.ForeignKey(
        verbose_name=_("Order"),
        to=Order,
        related_name="items",
        on_delete=models.CASCADE,
    )
    product = models.ForeignKey(
        verbose_name=_("Product"), to=Product, on_delete=models.SET_NULL, null=True
    )
    quantity = models.PositiveSmallIntegerField()

    class Meta:
        verbose_name = "Order item"
        verbose_name_plural = "Order items"

    # def clean(self):
    #     if self.quantity > self.product.quantity:
    #         raise ValidationError(
    #             "Quantity cannot be greater than the product balance."
    #         )

    def save(self, *args, **kwargs):
        # self.clean()
        super().save(*args, **kwargs)

        self.product.quantity -= self.quantity
        self.product.save()

    def __str__(self):
        return f"{self.product}-{self.quantity}"
