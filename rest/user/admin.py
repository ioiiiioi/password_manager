from django.contrib import admin
from core.models import User
# Register your models here.

@admin.register(User)
class UserAdmin(admin.ModelAdmin):

    search_fields = [
        'username', 
        'first_name',
        'email',
        'last_name'
    ]

    list_display = [
        'username',
        'email',
        'plan',
        'is_staff',
        'is_active',
    ]

    list_filter = [
        'is_active',
        'is_staff',
        'plan',
        'is_superuser'
    ]