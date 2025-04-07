from typing import Any
from django.contrib import admin
from core.models import Vault, VaultType
# Register your models here.

@admin.register(Vault)
class VaultAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'created_at',
        'updated_at',
    ]
    list_filter = [
        'vault_type',
        'created_by',
        'shared_team',
        'shared_organization',
    ]
    search_fields = [
        'name'
    ]

    fieldsets = [
        (
            "Data",
            {
                "fields":[
                    ('name',),
                    ('vault_type',),
                    ('username_readonly',),
                    ('password_readonly',),
                    ('url_readonly',),
                ]
            }
        ),
        (
            "Shared",
            {
                "fields":[
                ('shared_team',),
                ('shared_organization',),      
                ]
            }
        ),
        (
            "Details", 
            {
                'fields':[
                        ('value',),
                        ('created_by',),
                    ]
            }
        )
    ]

    readonly_fields=['password_readonly', "url_readonly", "username_readonly"]

    def username_readonly(self, instance):
        value = instance.value.get('username', None)
        return value if value else instance.value.get("email", None)
    
    username_readonly.short_description = 'username'

    def url_readonly(self, instance):
        return instance.value.get('url', None)
    
    url_readonly.short_description = 'url'
    
    def password_readonly(self, instance):
        return instance.value.get('password', None)

    password_readonly.short_description = 'password'

    def save_model(self, request, obj, form, change) -> None:
        if not change:
            obj.created_by = request.user
        else:
            obj.updated_by = request.user
        obj.save()

@admin.register(VaultType)
class VaultTypeAdmin(admin.ModelAdmin):
    list_display = [
        'name'
    ]
    search_fields = [
        'id'
        'name',
    ]