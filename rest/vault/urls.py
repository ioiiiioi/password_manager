from django.urls import path

from rest.vault.views import (
    ListVault,
    CreateEmailCredentials,
    CreateUsernameCredentials,
)

urlpatterns = [
    path('list/', ListVault.as_view(), name='list-vault'),
    path('create/credentials/email-based', CreateEmailCredentials.as_view(), name='create-email-credentials'),
    path('create/credentials/username-based', CreateUsernameCredentials.as_view(), name='create-username-credentials'),
    # path('password/change/', UserChangePassword.as_view(), name='user-change-password'),
]