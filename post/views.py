from rest_framework import generics, permissions
from .models import Post
from .serializers import PostSerializer
from .permissions import IsAuthorOrAdmin


class PostCreateView(generics.CreateAPIView):
    """Создание поста (CREATE)"""
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class PostListView(generics.ListAPIView):
    """Просмотр списка постов (READ)"""
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.AllowAny]


class PostDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Просмотр/редактирование/удаление поста (READ/UPDATE/DELETE)"""
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthorOrAdmin]

    def get_permissions(self):
        if self.request.method in ['GET']:
            return [permissions.AllowAny()]
        return [IsAuthorOrAdmin()]
