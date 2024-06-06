# views.py
from rest_framework.views import APIView
from rest_framework import mixins, viewsets, status, permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework_simplejwt.tokens import RefreshToken

from src.views import MultiSerializerMixin

from .models import User, OTP
from .serializers import (
    SendOTPSerializer,
    VerifyOTPSerializer,
    UserSerializer,
    MeUserSerializer,
)
from .utils import send_sms


class SendOTPView(APIView):
    """
    This view sends OTP(One Time Password) code to user
    """

    permission_classes = [permissions.AllowAny]

    def post(self, request):

        serializer = SendOTPSerializer(data=request.data)
        if serializer.is_valid():
            phone_number = serializer.validated_data["phone_number"]
            user, created = User.objects.get_or_create(phone_number=phone_number)
            otp = OTP.objects.create(user=user)
            otp.generate_otp()
            send_sms(
                phone_number=phone_number,
                message=f"This is test from Eskiz",
            )
            return Response(
                {"message": f"OTP {otp.otp_code} sent"}, status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VerifyOTPView(APIView):
    """
    This view verifies OTP(One Time Password) code from user
    and returns JWT access and refresh tokens
    """

    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = VerifyOTPSerializer(data=request.data)
        if serializer.is_valid():
            phone_number = serializer.validated_data["phone_number"]
            otp_code = serializer.validated_data["otp_code"]
            try:
                user = User.objects.get(phone_number=phone_number)
                otp = OTP.objects.filter(user=user, otp_code=otp_code).first()
                if otp and otp.is_valid():
                    refresh = RefreshToken.for_user(user)
                    return Response(
                        {
                            "refresh": str(refresh),
                            "access": str(refresh.access_token),
                        }
                    )
                return Response(
                    {"message": "Invalid OTP"}, status=status.HTTP_400_BAD_REQUEST
                )
            except User.DoesNotExist:
                return Response(
                    {"message": "User not found"}, status=status.HTTP_404_NOT_FOUND
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(MultiSerializerMixin, viewsets.ModelViewSet):
    """
    User model viewset
    """

    queryset = User.objects.all()
    serializer_class = UserSerializer
    serializer_action_classes = {"me": MeUserSerializer}
    permission_classes = [permissions.IsAdminUser]

    def get_permissions(self):
        if self.action == "me":
            self.permission_classes = [permissions.IsAuthenticated]
        else:
            self.permission_classes = super().permission_classes

        return super(UserViewSet, self).get_permissions()

    def get_object(self):
        if self.action == "me":
            return self.request.user
        return super().get_object()

    @action(url_path="me", detail=False, methods=["GET", "PUT", "PATCH"])
    def me(self, request, *args, **kwargs):
        if request.method == "GET":
            return super().retrieve(request, *args, **kwargs)
        elif request.method == "PUT":
            return super().update(request, *args, **kwargs)
        elif request.method == "PATCH":
            return super().partial_update(request, *args, **kwargs)
        else:
            return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
