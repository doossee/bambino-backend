from rest_framework import routers

from .views import BrandViewSet, CategoryViewSet, ProductViewSet


router = routers.DefaultRouter()

router.register(r"brands", BrandViewSet, basename="brand")
router.register(r"categories", CategoryViewSet, basename="category")
router.register(r"products", ProductViewSet, basename="product")
