from django.urls import path
from .views import SignUpView

urlpatterns = [
    # 회원가입
    path('api/signup/', SignUpView.as_view(), name='signup'),
]