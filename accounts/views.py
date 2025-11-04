from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import SignUpSerializers
from rest_framework.permissions import AllowAny
from accounts.emails.code_caches import verify_code, clear_code
from accounts.emails.email_services import EmailVerificationService
from django.contrib.auth import get_user_model


# 회원가입(아직 이메일 미 인증 버전)
class SignUpView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = SignUpSerializers(data=request.data)
        if serializer.is_valid():
            try:
                user = serializer.save()
                user.is_active = False
                user.save()

                signup_email_code = EmailVerificationService.email_service(user.email)

                return Response({"signup_email_code" : signup_email_code}, status=status.HTTP_201_CREATED)
            
            # 예외처리
            except Exception as e:
                return Response(
                    {"detail": f"회원가입 중 오류가 발생했습니다: {str(e)}"},
                    status=status.HTTP_400_BAD_REQUEST
                )

class EmailVerifyView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get("email")
        code = request.data.get("code")
        if not verify_code(email, code):
            return Response({"detail": "인증번호가 틀렸거나 만료되었습니다."}, status=status.HTTP_400_BAD_REQUEST)
        # 입력한 코드 가 맞을경우
        clear_code(email)
        user = get_user_model().objects.get(email=email)
        user.activate()
        return Response({"성공":"회원가입 완료"}, status=status.HTTP_201_CREATED)