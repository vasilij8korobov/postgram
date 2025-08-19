from django.urls import path

from comment.views import CommentCreateView, CommentListView, CommentDetailView

urlpatterns = [
    path('comments/create/', CommentCreateView.as_view()),
    path('comments/', CommentListView.as_view()),
    path('comments/<int:pk>/', CommentDetailView.as_view()),
]
