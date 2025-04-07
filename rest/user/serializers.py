from types import NoneType
import uuid
from rest_framework import serializers
from core.models import User
from core.base_models import READ_ONLY_FIELDS_WITH_DELETE
from utils.exceptions import BadRequestExceptions, UnauthorizedExceptions
from utils.middleware import UserAuthentication
from django.db import models
from django.contrib.auth.hashers import check_password, make_password

from utils.user_utils import UsernameRandomizer

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    email = serializers.EmailField(required=True)
    username = serializers.CharField(required=False, allow_null=True)

    def validate(self, attrs):
        username = attrs.get('username', None)
        if not username:
            username = UsernameRandomizer(attrs).generate_username()
            attrs['username'] = username
        # TODO : This will be temporary until we have email verificaiton method
        attrs['is_active'] = True
        attrs['password'] = make_password(attrs.get('password'))
        return super().validate(attrs)

    class Meta:
        model = User
        fields = [
            "email", 
            "username", 
            "password",
        ]

class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "last_login",
            "username",
            "first_name",
            "last_name",
            "email",
            "date_joined",
            "is_active",
            "is_sandbox",
            "created_at",
            "updated_at",
            "deleted_at",
            "private_metadata",
            "public_metadata",
            "plan",
            "phone_number",
            "organization",
            "groups",
            "user_permissions",
        ]
        read_only_fields = fields

class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True, write_only=True)

    def validate(self, attrs):
        self.token = None
        self.user = None
        user, token = UserAuthentication(username=attrs.get('email'), password=attrs.get('password')).authenticate
        self.token = token
        self.user = user
        return attrs

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        fields = [
            "id",
            "username",
            "first_name",
            "last_name",
            "organization",
            "plan",
            "phone_number",
            "is_active",
            "is_sandbox",
        ]
        for field in fields:
            attr = getattr(self.user, field, None)
            if isinstance(attr, str) or isinstance(attr, bool) or isinstance(attr, int):
                ret[field] = attr
            elif isinstance(attr, uuid.UUID):
                ret[field] = str(attr)
            elif isinstance(attr, models.Model):
                ret[field] = attr.__str__
            elif isinstance(attr, NoneType):
                ret[field] = None
        ret['token'] = self.token
        return ret 

class UserChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True, write_only=True)
    new_password = serializers.CharField(required=True, write_only=True)

    def validate_old_password(self, attrs):
        return attrs

    def validate_new_password(self, attrs):
        return attrs

    def validate(self, attrs):
        request = self.context.get('request', None)
        if not request:
            raise BadRequestExceptions(detail="Request origin could not be found.")
        if request.user.is_anonymous:
            raise UnauthorizedExceptions(detail="Must login to change the password.")
        if not check_password(attrs['old_password'], request.user.password):
            raise UnauthorizedExceptions(detail="Wrong old password.")
        return attrs
    
    def update(self, instance, validated_data):
        validated_data.pop('old_password')
        instance.password = make_password(validated_data.pop('new_password'))
        instance.save()
        # TODO : add blocked old token here also
        return instance