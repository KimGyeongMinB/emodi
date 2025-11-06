from django.db import models
from django.conf import settings

# 공지사항/문의게시판 Post 앱
# 11/06 할거 공지사항(관리자 전용)/문의게시판 태그 만들기
class Post(models.Model):

    # announcement - 관리자
    # inquiry - 문의게시판
    TAG_CHOICES = [
        ("announcement", "Announcement"),
        ("inquiry", "Inquiry")
    ]
    tags = models.CharField(max_length=12, choices=TAG_CHOICES, default='inquiry')
    title = models.CharField(max_length=20)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='posts', on_delete=models.CASCADE)