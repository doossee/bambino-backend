from django.db import models
from modeltrans.fields import TranslationField
from mptt.models import MPTTModel, TreeForeignKey
from django.contrib.auth import get_user_model

User = get_user_model()

class AbstractProductModel(models.Model):

    """Abstract Product Model"""

    title = models.CharField(max_length=100)
    description = models.TextField()
    usage = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    i18n = TranslationField(fields=('description', 'usage'), required_languages=('ru','uz'))

    class Meta:
        abstract = True


class Brand(models.Model):

    """Brand model"""

    name = models.CharField(max_length=100)
    description = models.TextField()
    image = VersatileImageField(
        'Image',
        upload_to='images/',
        ppoi_field='image_ppoi'
    )
    image_ppoi = PPOIField()

    i18n = TranslationField(fields=('description',))

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Brand'
        verbose_name_plural = 'Brands'


class Category(MPTTModel):

    """Category model"""

    name = models.CharField(max_length=100)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)

    i18n = TranslationField(fields=('name',))

    def __str__(self):
        return self.name

    class MPTTMeta:
        order_insertion_by = ['name']
    
    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'



class Product(AbstractProductModel):
    
    """Product model"""
    
    title = models.CharField(max_length=100)
    description = models.TextField()
    usage = models.TextField()

    category = models.ForeignKey(to=Category, related_name='products', null=True, on_delete=models.SET_NULL)
    brand = models.ForeignKey(to=Brand, null=True, on_delete=models.SET_NULL)
    
    price = models.DecimalField(max_digits=11, decimal_places=2)
    discount = models.PositiveSmallIntegerField()

    is_published = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'


class ProductUnit(models.Model):

    """Product unit model"""

    product = models.ForeignKey(to=Product, related_name='units', on_delete=models.CASCADE)
    balance = models.PositiveBigIntegerField(editable=False, default=0)
    image = VersatileImageField(
        'Image',
        upload_to='images/',
        ppoi_field='image_ppoi'
    )
    image_ppoi = PPOIField()

    class Meta:
        unique_together = ('product', 'color')


class Image(models.Model):

    """Image model"""

    product = models.ForeignKey(to=Product, related_name='images', on_delete=models.CASCADE)
    image = VersatileImageField(
        'Image',
        upload_to='images/',
        ppoi_field='image_ppoi'
    )
    image_ppoi = PPOIField()

    def __str__(self):
        return f'{self.product.title}-{self.id} image'
    
    class Meta:
        verbose_name = 'Image'
        verbose_name_plural = 'Images'


class Rating(models.Model):

    """Rating model"""

    RATE_CHOICES = (
        (1, 'Ok'),
        (2, 'Fine'),
        (3, 'Good'),
        (4, 'Amazing'),
        (5, 'Incredible')
    )
    user = models.ForeignKey(to=User, related_name='ratings', on_delete=models.CASCADE)
    product = models.ForeignKey(to=Product, related_name='ratings', on_delete=models.CASCADE)
    rate = models.PositiveSmallIntegerField(choices=RATE_CHOICES)
    review = models.TextField()


    def __str__(self):
        return f'{self.user}-{self.product}-{self.rate}'

    class Meta:
        verbose_name = 'Rating'
        verbose_name_plural = 'Ratings'
