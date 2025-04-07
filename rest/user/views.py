from rest_framework import permissions, response, authentication
from rest_framework.generics import (
    CreateAPIView,
    ListAPIView,
    UpdateAPIView,
    RetrieveAPIView,
)
from django.contrib.auth.hashers import make_password
from core.models import User
from .serializers import (
    UserRegistrationSerializer,
    UserLoginSerializer,
    UserDetailSerializer,
    UserChangePasswordSerializer,
)

class UserCreateAPI(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    authentication_classes = []
    permission_classes = [permissions.AllowAny]

class UserLoginAPI(CreateAPIView):
    queryset = User.objects.all()
    authentication_classes = []
    serializer_class = UserLoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return response.Response(serializer.data)

class UserListAPI(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserDetailSerializer
    permission_classes = [permissions.IsAdminUser]

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user.organization:
            self.queryset = self.queryset.filter(organization=request.user.organization)
        if request.user.is_anonymous:
            self.queryset = self.queryset.none()
        return super().get(request, *args, **kwargs)

class UserChangePassword(UpdateAPIView):
    queryset = User.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserChangePasswordSerializer
    http_method_names = ['patch']
    
    def patch(self, request, *args, **kwargs):
        self.kwargs['pk'] = self.request.user.pk
        return super().patch(request, *args, **kwargs)


