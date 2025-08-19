from django.urls import path

from post.views import PostCreateView, PostListView, PostDetailView

urlpatterns = [
    path('posts/create/', PostCreateView.as_view()),
    path('posts/', PostListView.as_view()),
    path('posts/<int:pk>/', PostDetailView.as_view()),
]
