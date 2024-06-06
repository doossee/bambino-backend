from django.http import Http404

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser

from src.views import MultiSerializerMixin

from .models import (
    Brand,
    Category,
    Product,
    ProductImage,
)
from .serializers import (
    BrandSerializer,
    AbstractCategorySerializer,
    CategoryTreeSerializer,
    ProductImageSerializer,
    ProductSerializer,
    ProductReadSerializer,
)
from .filters import ProductFilter
from .permissions import ReadOnly


class BrandViewSet(viewsets.ModelViewSet):
    """
    Brand model viewset
    """

    queryset = Brand.objects.all()
    serializer_class = BrandSerializer
    # permission_classes = [IsAdminUser | ReadOnly]


class CategoryViewSet(MultiSerializerMixin, viewsets.ModelViewSet):
    """
    Category model viewset
    """

    queryset = Category.objects.all()
    serializer_action_classes = {
        "default": AbstractCategorySerializer,
        "list_tree": CategoryTreeSerializer,
    }
    # permission_classes = [IsAdminUser | ReadOnly]
    search_fields = [
        "name",
    ]

    @action(detail=False, methods=["GET"])
    def list_tree(self, request):
        queryset = Category.objects.all().select_related("parent").filter(parent=None)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class ProductViewSet(MultiSerializerMixin, viewsets.ModelViewSet):
    """
    Product model viewset"""

    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    serializer_action_classes = {
        "list": ProductReadSerializer,
        "retrieve": ProductReadSerializer,
        "create_image": ProductImageSerializer,
    }
    # permission_classes = [IsAdminUser | ReadOnly]
    filterset_class = ProductFilter
    search_fields = [
        "title",
    ]
    lookup_field = "slug"

    @action(detail=True, methods=["post"])
    def create_image(self, request, slug=None):
        product = self.get_object()

        image_data = request.data.get("image")
        if not image_data:
            return Response(
                {"detail": "Image data is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Use ProductImageSerializer for the image
        serializer = ProductImageSerializer(
            data={"product": product.id, "image": image_data}
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=["delete"])
    def delete_image(self, request, slug=None, image_id=None):
        product = self.get_object()

        try:
            image = ProductImage.objects.get(id=image_id, product=product)
        except ProductImage.DoesNotExist:
            return Response(
                {"detail": "Image not found."}, status=status.HTTP_404_NOT_FOUND
            )

        image.delete()
        return Response(
            {"detail": "Image deleted successfully."}, status=status.HTTP_204_NO_CONTENT
        )

    def get_queryset(self):
        qs = (
            super()
            .get_queryset()
            .select_related(
                "category",
                "brand",
            )
            .prefetch_related("images")
        )
        return qs
