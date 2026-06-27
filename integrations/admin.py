from django.contrib import admin
from .models import Integration


@admin.register(Integration)
class IntegrationAdmin(admin.ModelAdmin):
    list_display = ('company', 'name', 'integration_type', 'status', 'is_active', 'last_sync_at')
    list_filter = ('integration_type', 'status', 'is_active', 'company')
    search_fields = ('company__name', 'name', 'base_url', 'username')
