from django.urls import path
from .views import SignUpView, EmailVerifyView, ResetPasswordView, VerifyResetPassword

urlpatterns = [
    # 회원가입
    path('api/signup/', SignUpView.as_view(), name='signup'),
    path('api/emailcodeverify/', EmailVerifyView.as_view(), name='verifyemail'),

    # 비밀번호 리셋(아예 잊어버렸을때)
    path('api/resetpassword/', ResetPasswordView.as_view(), name='resetpassword'),

    # 비밀번호 입력(아예 잊어버렸을때)
    path('api/newpassword/', VerifyResetPassword.as_view(), name='newpassword')
]