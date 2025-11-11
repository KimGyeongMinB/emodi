# 조회수 모델
from django.db import models
from django.conf import settings
from django.db.models import F
from django.utils import timezone
from posts.models import Post

class PostViewCountModel(models.Model):
    post = models.ForeignKey(Post, related_name="view_counter", on_delete=models.CASCADE)
    view_count = models.IntegerField(default=0, verbose_name="조회수")
    day = models.DateField(db_index=True, default=timezone.localdate)
    view_date = models.DateTimeField(auto_now_add=True)
    view_user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='viewed_posts', on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["post", "view_user", "day"], name="uniq_post_user_day")
        ]

    def increment(self):
        PostViewCountModel.objects.filter(pk=self.pk).update(
            view_count=F("view_count") + 1
        )
        self.refresh_from_db(fields=["view_count"])
        return self.view_count