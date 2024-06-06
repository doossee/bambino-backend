from django.urls import path
from rest_framework import routers
from rest_framework_simplejwt.views import TokenRefreshView

from .views import SendOTPView, VerifyOTPView, UserViewSet

router = routers.DefaultRouter()

router.register(r'users', UserViewSet, basename='user')

urlpatterns = router.urls

urlpatterns += [
    path("send_otp/", SendOTPView.as_view(), name="send_otp"),
    path("verify_otp/", VerifyOTPView.as_view(), name="verify_otp"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]