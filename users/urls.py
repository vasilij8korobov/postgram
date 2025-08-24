from django.urls import path
from .views import UserCreateView, UserListView, UserDetailView, CustomAuthToken

urlpatterns = [
    path('register/', UserCreateView.as_view(), name='user-register'),
    path('token/login/', CustomAuthToken.as_view(), name='api-token-auth'),
    path('', UserListView.as_view(), name='user-list'),
    path('<int:pk>/', UserDetailView.as_view(), name='user-detail'),
]
