from django.urls import path

from users.views import UserCreateView, UserListView, UserDetailView

urlpatterns = [
    path('users/register/', UserCreateView.as_view()),
    path('users/', UserListView.as_view()),
    path('users/<int:pk>/', UserDetailView.as_view()),
]
