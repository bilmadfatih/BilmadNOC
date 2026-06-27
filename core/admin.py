from django.contrib import admin
from .models import Company, Location, Workspace


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('name', 'short_name', 'health_score', 'is_active', 'created_at')
    search_fields = ('name', 'short_name')
    list_filter = ('is_active',)


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ('company', 'name', 'is_active')
    search_fields = ('company__name', 'name')
    list_filter = ('company', 'is_active')


@admin.register(Workspace)
class WorkspaceAdmin(admin.ModelAdmin):
    list_display = ('name', 'workspace_type', 'can_view_it', 'can_view_network', 'can_view_cctv', 'can_view_alarm')
    list_filter = ('workspace_type', 'can_view_it', 'can_view_network', 'can_view_cctv', 'can_view_alarm')
    filter_horizontal = ('users', 'companies')
