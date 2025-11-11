from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import (SignUpSerializers, ResetVerifySerializer
                            ,SignupEmailSerializer, ResetPasswordSerializer)
from rest_framework.permissions import AllowAny
from accounts.emails.signup_email_services import EmailVerificationService
from accounts.password.new_password_email_services import PasswordVerificationService


# 회원가입
class SignUpView(APIView):
    """
    회원가입 뷰
    이메일, 패스워드, 닉네임 입력후 전송 시
    회원가입 인증 코드 발송
    is_active = True 에서 False 로 전환
    """
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = SignUpSerializers(data=request.data)
        if serializer.is_valid():
            try:
                user = serializer.save()
                user.save()
                signup_email_code = EmailVerificationService.email_service(user.email)
                return Response({"signup_email_code" : signup_email_code}, status=status.HTTP_201_CREATED)
            
            # 예외처리
            except Exception as e:
                return Response(
                    {"detail": f"회원가입 중 오류가 발생했습니다: {str(e)}"},
                    status=status.HTTP_400_BAD_REQUEST
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# 이메일 코드 인증
class EmailVerifyView(APIView):
    """
    회원가입 시 이메일 코드 인증하는 뷰
    email, code 입력
    입력 성공시 모델 메서드에서 True 로 전환
    """
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = SignupEmailSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({"성공": "회원가입 완료"}, status=status.HTTP_201_CREATED)
        return Response({"detail": "회원가입 실패."}, status=status.HTTP_400_BAD_REQUEST)

# ------------- 구분선 ------------- #

# 비밀번호를 아예 잊어버렸을때
# 패스워드 리셋을 위한 이메일 입력 뷰
class ResetPasswordView(APIView):
    """
    비로그인 시 사용가능
    패스워드 리셋을 위한 이메일 입력 뷰
    이메일 입력 -> 이메일 발송
    """
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = ResetPasswordSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            password_find_code = PasswordVerificationService.password_email_service(serializer.validated_data["email"])

            return Response(
                {"password_find_code": password_find_code},
                status=status.HTTP_201_CREATED
            )
        else:
            return Response(
                {"password_find_code": '실패'},
                status=status.HTTP_400_BAD_REQUEST
            )

# 새 비밀번호 입력
class VerifyResetPassword(APIView):
    """
    이메일, 인증코드, 비밀번호 같이 입력
    """
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = ResetVerifySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"성공":"비밀번호 재설정"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
