from django.urls import path
from .views import PostListView, PostCreateView, PostpatchView, PostDeleteView, PostDetailView

urlpatterns = [
    # 회원가입
    path('api/list/all_post/', PostListView.as_view(), name='postlist'),
    path('api/create/post/', PostCreateView.as_view(), name='postcreate'),
    path('api/datail/post/<int:post_id>/', PostDetailView.as_view(), name='postdatail'),
    path('api/update/post/<int:post_id>/', PostpatchView.as_view(), name='postupdate'),
    path('api/detailview/post/<int:post_id>/delete/', PostDeleteView.as_view(), name='postdelete')
]