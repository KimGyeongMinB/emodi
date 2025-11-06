from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from .models import Post
from .serializers import PostSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.exceptions import PermissionDenied
from paginations.paginations import StandardResultsSetPagination

# 할거
"""
1. 수정(완료)
2. 삭제(완료)
3. 글 상세페이지(완료)
3. 페이지네이션(완료)
"""

# 문의/공지사항 전체 리스트
class PostListView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        """
        최신글 순으로 정렬
        페이지네이션 클래스 불러오기
        페이지네이션 PageNumberPagination 부모클래스 안의 함수 paginate_queryset
        (self, queryset, request, view=None) 에서 self 는 StandardResultsSetPagination().
        """
        posts = Post.objects.all().order_by('-created_at')
        page_qs = StandardResultsSetPagination().paginate_queryset(posts, request, view=self)

        serializer = PostSerializer(page_qs, many=True)
        if serializer:
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# 문의/공지사항 생성
class PostCreateView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = PostSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# 문의/공지사항 상세페이지 뷰
# 상세페이지 불러오기/수정(글쓴이만)
class PostDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, post_id):
        """
        글 상세페이지 불러오기
        """
        post = get_object_or_404(Post, id=post_id)
        if not post:
            return Response({"Not Found" : "글을 찾을수 없습니다"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = PostSerializer(post)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, post_id):
        """
        글 수정
        context = 시리얼라이저에 추가 정보 제공
        코드 리팩토링간 통일성을 위해 시리얼라이저에서 유저검증 로직 추가
        """
        post = get_object_or_404(Post, id=post_id)

        context = {
            'post': post,
            'request': request
        }

        serializer = PostSerializer(instance=post, data=request.data, context=context, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# 글 삭제
class PostDeleteView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    # lookup_field = "DB 에 저장되어 있는 필드"
    # lookup_url_kwarg = "URL 에 넣을 이름"

    lookup_field = "id"
    lookup_url_kwarg = "post_id"

    """
    DestroyAPIView 안의 DestroyModelMixin 에서 def delete 함수 커스터마이징(응답관련)
    perform_destroy 도 조건문 추가
    """

    def delete(self, request, *args, **kwargs):
        data = self.destroy(request, *args, **kwargs)
        return Response(
            {"detail": "게시글이 성공적으로 삭제되었습니다."},
            status=status.HTTP_200_OK
        ) 

    def perform_destroy(self, instance):
        if instance.author != self.request.user:
            raise PermissionDenied("작성자만 삭제할 수 있습니다.")
        instance.delete()