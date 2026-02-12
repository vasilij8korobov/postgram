from rest_framework import generics, permissions
from .models import Comment
from .serializers import CommentSerializer
from .permissions import IsAuthorOrAdmin


class CommentCreateView(generics.CreateAPIView):
    """Создание комментария (CREATE)"""
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentListView(generics.ListAPIView):
    """Просмотр списка комментариев (READ)"""
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.AllowAny]


class CommentDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Просмотр/редактирование/удаление комментария (READ/UPDATE/DELETE)"""
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthorOrAdmin | permissions.IsAdminUser]
