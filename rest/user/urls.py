from django.urls import path
from .views import (
    UserCreateAPI,
    UserLoginAPI,
    UserListAPI,
    UserChangePassword,
)

urlpatterns = [
    path('sign-up/', UserCreateAPI.as_view(), name='user-registration'),
    path('login/', UserLoginAPI.as_view(), name='user-login'),
    path('list/', UserListAPI.as_view(), name='user-list'),
    path('password/change/', UserChangePassword.as_view(), name='user-change-password'),
]