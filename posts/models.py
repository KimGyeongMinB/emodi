from django.db import models
from django.conf import settings
from django.db.models import F
from django.utils import timezone
from posts.postsquerysets import PostQuerySet
from posts.post_viewcount import PostViewCountModel


class PostManager(models.Manager):
    def get_queryset(self):
        return PostQuerySet(self.model, using=self._db)

    # 전체조회수 불러오기
    def with_view_count(self):
        return self.get_queryset().with_view_count()
    
    # 1일 조회수 불러오기
    def with_today_view_count(self):
        return self.get_queryset().with_today_view_count()


# 공지사항/문의게시판 Post 앱
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

    objects = PostManager()

    def __str__(self):
        return self.title
    
    # 총 조회수
    def get_increment(self, user=None, day=None):
        day = timezone.localdate()
        view_user = user if user.is_authenticated else None
        counter, created  = PostViewCountModel.objects.get_or_create(post=self, view_user=view_user, day=day)
        if not created:
            pass
        
        counter.increment()

        return (
            type(self)
            .objects
            .with_view_count()
            .with_today_view_count()
            .select_related("author")
            .get(pk=self.pk)
        )