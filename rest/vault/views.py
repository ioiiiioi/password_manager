from urllib import request
from rest_framework.generics import (
    ListAPIView,
    RetrieveAPIView,
    CreateAPIView,
)
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions, filters
from drf_spectacular.utils import extend_schema
from core.models.vault import Vault
from rest.vault.serializers import CreateEmailCredetialsSerializer, CreateUsernameCredetialsSerializer, VaultRetrieveSerializer

# Create your views here.

class ListVault(ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Vault.objects.all()
    serializer_class = VaultRetrieveSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['name',]
    search_fields = ['name']

    def get_queryset(self):
        return self.queryset.filter(created_by=self.request.user)

@extend_schema(
    request=CreateUsernameCredetialsSerializer(many=True)
)    
class CreateEmailCredentials(CreateAPIView):
    serializer_class = CreateEmailCredetialsSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Vault.objects.all()

    def get_serializer(self, *args, **kwargs):
        kwargs['many'] = isinstance(self.request.data, list)
        return super().get_serializer(*args, **kwargs)

@extend_schema(
    request=CreateUsernameCredetialsSerializer(many=True)
)
class CreateUsernameCredentials(CreateAPIView):
    serializer_class = CreateUsernameCredetialsSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Vault.objects.all()

    def get_serializer(self, *args, **kwargs):
        kwargs['many'] = isinstance(self.request.data, list)
        return super().get_serializer(*args, **kwargs)