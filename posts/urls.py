from django.urls import path
from .views import PostListView, PostCreateView, PostDetailView, PostDeleteView

urlpatterns = [
    # 회원가입
    path('api/list/all_post/', PostListView.as_view(), name='postlist'),
    path('api/create/post/', PostCreateView.as_view(), name='postcreate'),
    path('api/detailview/post/<int:post_id>/', PostDetailView.as_view(), name='postdetail'),
    path('api/detailview/post/<int:post_id>/delete/', PostDeleteView.as_view(), name='postdelete')
]