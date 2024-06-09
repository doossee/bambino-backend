from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify

from mptt.models import MPTTModel, TreeForeignKey

from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill

from src.models import Extensions, TimeStampedModel


User = get_user_model()


def brand_image_path(instance, filename):
    return f"uploads/brands/{instance.name}/{filename}"


def category_image_path(instance, filename):
    return f"uploads/categories/{instance.name}/{filename}"


def product_image_path(instance, filename):
    return f"uploads/products/{instance.product.title}/{filename}"




class Brand(models.Model):
    """
    Brand model
    """

    name = models.CharField(verbose_name=_("Name"), max_length=255)
    description = models.TextField(verbose_name=_("Description"), blank=True)
    icon = models.ImageField(upload_to=brand_image_path, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Brand")
        verbose_name_plural = _("Brands")


class Category(MPTTModel):
    """
    Category model
    """

    name = models.CharField(verbose_name=_("Name"), max_length=255)
    icon = models.ImageField(upload_to=category_image_path, blank=True)
    parent = TreeForeignKey(
        verbose_name=_("Parent category"),
        to="self",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    created_at = models.DateTimeField(
        verbose_name=_("Created at"), db_index=True, auto_now_add=True
    )
    updated_at = models.DateTimeField(verbose_name=_("Updated at"), auto_now=True)

    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")

    def __str__(self):
        return self.name


class Product(Extensions):
    """
    Product model
    """

    title = models.CharField(verbose_name=_("Title"), max_length=255)
    # slug = models.SlugField(verbose_name=_("Slug"), null=True, blank=True)
    description = models.TextField(verbose_name=_("Description"), blank=True)

    category = TreeForeignKey(
        verbose_name=_("Category"),
        to=Category,
        related_name="products",
        null=True,
        on_delete=models.SET_NULL,
    )
    brand = models.ForeignKey(
        verbose_name=_("Brand"),
        to=Brand,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
    )

    quantity = models.IntegerField(verbose_name=_("Quantity"), default=1)
    price = models.DecimalField(
        verbose_name=_("Price"), max_digits=11, decimal_places=2
    )
    discount = models.PositiveSmallIntegerField(
        verbose_name=_("Discount"), default=0, blank=True
    )

    views = models.PositiveIntegerField(verbose_name=_("Views"), default=0)
    is_deleted = models.BooleanField(verbose_name=_("Is deleted"), default=False)

    class Meta:
        verbose_name = _("Product")
        verbose_name_plural = _("Products")

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.pk:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)


class ProductImage(models.Model):
    """
    Product images model
    """

    product = models.ForeignKey(
        to=Product,
        related_name="images",
        on_delete=models.CASCADE,
        verbose_name=_("Product"),
    )
    image = models.ImageField(
        verbose_name=_("Image"),
        upload_to=product_image_path,
    )
    thumbnail = ImageSpecField(
        source="image",
        processors=[ResizeToFill(100, 100)],
        format="WEBP",
        options={"quality": 60},
    )

    def __str__(self):
        return f"{self.product.title}-{self.id} image"

    class Meta:
        verbose_name = _("Image")
        verbose_name_plural = _("Images")


class ProductView(TimeStampedModel):
    """
    Product views model
    """

    ip = models.CharField(verbose_name=_("IP address"), max_length=255)
    product = models.ForeignKey(
        Product, related_name="product_views", on_delete=models.CASCADE
    )

    class Meta:
        verbose_name = _("Product view")
        verbose_name_plural = _("Product views")


class Review(models.Model):
    """
    Rating model
    """

    RATE_CHOICES = (
        (1, _("Ok")),
        (2, _("Fine")),
        (3, _("Good")),
        (4, _("Amazing")),
        (5, _("Incredible")),
    )
    user = models.ForeignKey(
        verbose_name=_("User"),
        to=User,
        related_name="ratings",
        on_delete=models.CASCADE,
    )
    product = models.ForeignKey(
        to=Product,
        related_name="ratings",
        on_delete=models.CASCADE,
        verbose_name=_("Product"),
    )
    rate = models.PositiveSmallIntegerField(_("Rate"), choices=RATE_CHOICES)
    text = models.TextField(_("Text"))

    def __str__(self):
        return f"{self.user}-{self.product}-{self.rate}"

    class Meta:
        verbose_name = _("Rating")
        verbose_name_plural = _("Ratings")
