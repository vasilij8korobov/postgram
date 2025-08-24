from django.urls import path
from .views import CommentCreateView, CommentListView, CommentDetailView

urlpatterns = [
    path('', CommentListView.as_view(), name='comment-list'),
    path('create/', CommentCreateView.as_view(), name='comment-create'),
    path('<int:pk>/', CommentDetailView.as_view(), name='comment-detail'),
]
