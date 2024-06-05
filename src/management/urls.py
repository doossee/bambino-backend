# urls.py
from django.urls import path
from .views import SendOTPView, VerifyOTPView

from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

urlpatterns = [
    path('send_otp/', SendOTPView.as_view(), name='send_otp'),
    path('verify_otp/', VerifyOTPView.as_view(), name='verify_otp'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh')
]
