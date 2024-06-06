import os
from rest_framework import serializers

from .models import Brand, Category, Product, ProductImage


class BrandSerializer(serializers.ModelSerializer):
    """
    Brand model serializer
    """

    class Meta:
        model = Brand
        fields = "__all__"


class AbstractCategorySerializer(serializers.ModelSerializer):
    """
    Abstract Category model serializer
    """

    class Meta:
        model = Category
        fields = [
            "id",
            "lft",
            "rght",
            "tree_id",
            "level",
            "name",
            "parent",
            "icon",
        ]


class CategoryExpandSerializer(AbstractCategorySerializer):
    """
    Category expand model serializer
    """

    class Meta(AbstractCategorySerializer.Meta):
        depth = 5


class CategoryTreeSerializer(AbstractCategorySerializer):
    """
    Category model serializer
    """

    children = serializers.SerializerMethodField()

    def get_children(self, instance):

        children = instance.get_children()
        serializer = CategoryTreeSerializer(children, many=True)
        return serializer.data

    class Meta(AbstractCategorySerializer.Meta):
        meta = AbstractCategorySerializer.Meta
        fields = meta.fields + ["children"]


class ProductImageSerializer(serializers.ModelSerializer):
    """
    Product image serialier
    """

    # thumbnail = serializers.SerializerMethodField()

    class Meta:
        model = ProductImage
        exclude = ["product",]
        # fields = [
        #     "id",
        #     "product_id",
        #     "image",
        #     "thumbnail",
        # ]

    # def to_representation(self, instance):
    #     data = super().to_representation(instance)

    #     if hasattr(instance, "image") and hasattr(instance.image, "url"):
    #         data["image"] = f"{os.getenv('MEDIA_PREFIX', '')}{instance.image.url}"

    #     return data

    # def get_thumbnail(self, obj):
    #     return os.getenv("MEDIA_PREFIX", "") + obj.thumbnail.url


class ProductSerializer(serializers.ModelSerializer):
    """
    Product default serializer
    """

    class Meta:
        model = Product
        fields = "__all__"


class ProductReadSerializer(serializers.ModelSerializer):
    """
    Product retrieve model serializer
    """

    brand = BrandSerializer()
    category = CategoryExpandSerializer()
    images = ProductImageSerializer()

    class Meta:
        model = Product
        fields = "__all__"
