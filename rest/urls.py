from django.urls import path, include

urlpatterns = [
    path('users/', include('rest.user.urls')),
    path('organization/', include('rest.organization.urls')),
    path('vault/', include('rest.vault.urls')),
]