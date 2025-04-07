from email.policy import default
from rest_framework import serializers
from core.models.vault import Vault, VaultType

class VaultRetrieveSerializer(serializers.ModelSerializer):

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        vault_type = instance.vault_type
        value_keys = vault_type.keys 
        for key in value_keys:
            ret[key.lower()] = instance.value.get(key.lower(), None)
        return ret

    class Meta:
        model = Vault
        fields = [
            'name',
            'created_at',
            'updated_at',
            'deleted_at',
        ]

class VaultCreateSerializer(serializers.ModelSerializer):
    created_by = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Vault
        fields = [
            'name',
            'created_by'
        ]

class CreateUsernameCredetialsSerializer(VaultCreateSerializer):
    username = serializers.CharField(write_only=True, required=True)
    password = serializers.CharField(write_only=True, required=True)
    url = serializers.CharField(write_only=True, required=False, allow_null=True)
    vault_type = serializers.HiddenField(default=VaultType.objects.get(name="USERNAME_BASED_LOGIN"))

    def validate(self, attrs):
        username = attrs.pop('username', None)
        password = attrs.pop('password', None)
        url = attrs.pop('url', None)
        attrs['value'] = {
            'username':username,
            'password':password,
            'url':url,
        }
        return attrs
    
    class Meta:
        model = Vault
        fields = [
            'name',
            'username',
            'password',
            'url',
            'vault_type',
            'created_by',
        ]
    
class CreateEmailCredetialsSerializer(VaultCreateSerializer):
    email = serializers.CharField(write_only=True, required=True)
    password = serializers.CharField(write_only=True, required=True)
    url = serializers.CharField(write_only=True, required=False, allow_null=True)
    vault_type = serializers.HiddenField(default=VaultType.objects.get(name="USERNAME_BASED_LOGIN"))

    def validate(self, attrs):
        email = attrs.pop('email', None)
        password = attrs.pop('password', None)
        url = attrs.pop('url', None)
        attrs['value'] = {
            'email':email,
            'password':password,
            'url':url,
        }
        return attrs
    
    class Meta:
        model = Vault
        fields = [
            'name',
            'email',
            'password',
            'url',
            'vault_type',
            'created_by',
        ]
    