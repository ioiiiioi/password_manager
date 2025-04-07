from django.contrib import admin
from core.models import Organization
# Register your models here.

@admin.register(Organization)
class OrgAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'alias',
        'plan',
    ]

    list_filter = [
        'plan',
    ]

    search_fields = [
        'name',
        'alias',
    ]