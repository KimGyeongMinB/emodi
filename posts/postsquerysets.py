from django.db import models
from django.db.models import Sum, Q
from django.db.models.functions import Coalesce
from django.utils import timezone

class PostQuerySet(models.QuerySet):
    # 전체 조회수
    def with_view_count(self):
        return self.prefetch_related("view_counter").annotate(
            view_count=Coalesce(Sum("view_counter__view_count"), 0)
        )
    
    # 1일 조회수
    def with_today_view_count(self):
        # day = 오늘날짜
        day = timezone.localdate()
        return self.prefetch_related("view_counter").annotate(
            view_count=Coalesce(Sum("view_counter__view_count", filter=Q(view_counter__day=day)), 0)
        )