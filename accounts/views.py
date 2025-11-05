from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import SignUpSerializers, ResetVerifySerializer
from rest_framework.permissions import AllowAny
from accounts.emails.signup_caches import verify_code, clear_code
from accounts.emails.signup_email_services import EmailVerificationService
from accounts.password.new_password_email_services import PasswordVerificationService
from django.contrib.auth import get_user_model


# 회원가입
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
        # 예외처리
        try:
            user = get_user_model().objects.get(email=request.data.get("email"))
        except get_user_model().DoesNotExist:
            return Response({"detail": "가입된 이메일이 존재하지 않습니다."}, status=status.HTTP_400_BAD_REQUEST)

        # 비밀번호 찾기 이메일 발송
        password_find_code = PasswordVerificationService.password_email_service(user.email)

        return Response(
            {"password_find_code": password_find_code},
            status=status.HTTP_201_CREATED
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
