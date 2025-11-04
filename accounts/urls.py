from django.urls import path
from .views import SignUpView, EmailVerifyView

urlpatterns = [
    # 회원가입
    path('api/signup/', SignUpView.as_view(), name='signup'),
    path('api/emailcodeverify/', EmailVerifyView.as_view(), name='verifyemail')
]