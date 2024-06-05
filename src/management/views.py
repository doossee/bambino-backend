# views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from .models import OTP
from .serializers import SendOTPSerializer, VerifyOTPSerializer
from rest_framework_simplejwt.tokens import RefreshToken


class SendOTPView(APIView):
    def post(self, request):
        serializer = SendOTPSerializer(data=request.data)
        if serializer.is_valid():
            phone_number = serializer.validated_data["phone_number"]
            try:
                user = User.objects.get(phone_number=phone_number)
                otp = OTP(user=user)
                otp.generate_otp()

                return Response({"message": "OTP sent"}, status=status.HTTP_200_OK)
            except User.DoesNotExist:
                return Response(
                    {"message": "User not found"}, status=status.HTTP_404_NOT_FOUND
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VerifyOTPView(APIView):
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
