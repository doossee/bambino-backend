from core.routers import DefaultRouter

from src.products.urls import router as products_router
from src.orders.urls import router as orders_router


router = DefaultRouter()

router.extend(products_router)
router.extend(orders_router)
