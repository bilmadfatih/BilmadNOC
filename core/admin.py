from django.contrib import admin
from .models import AuditLog, Company, Customer, Location, Site, Tenant, Workspace


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('name', 'short_name', 'health_score', 'is_active', 'created_at')
    search_fields = ('name', 'short_name')
    list_filter = ('is_active',)


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ('company', 'name', 'is_active')
    search_fields = ('company__name', 'name', 'address')
    list_filter = ('company', 'is_active')


@admin.register(Workspace)
class WorkspaceAdmin(admin.ModelAdmin):
    list_display = ('name', 'workspace_type', 'can_view_it', 'can_view_network', 'can_view_cctv', 'can_view_alarm')
    list_filter = ('workspace_type',)
    filter_horizontal = ('users', 'companies')


@admin.register(Tenant)
class TenantAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'is_active', 'created_at')
    search_fields = ('name', 'slug')


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'contact_name', 'contact_email', 'is_active')
    search_fields = ('name', 'code', 'contact_name', 'contact_email')
    list_filter = ('is_active', 'tenant')


@admin.register(Site)
class SiteAdmin(admin.ModelAdmin):
    list_display = ('name', 'customer', 'site_type', 'is_active')
    search_fields = ('name', 'customer__name')
    list_filter = ('site_type', 'is_active')


@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ('action', 'model_name', 'user', 'created_at')
    search_fields = ('model_name', 'message')
    list_filter = ('action', 'model_name')
    readonly_fields = ('uuid', 'created_at')
