from django.contrib import admin
from .models import Application, AssetRelationship, BackupJob, BusinessService, Dependency


class DependencyInline(admin.TabularInline):
    model = Dependency
    extra = 0
    autocomplete_fields = ('asset',)


@admin.register(BusinessService)
class BusinessServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'company', 'criticality', 'owner', 'is_active')
    list_filter = ('criticality', 'is_active', 'company')
    search_fields = ('name', 'company__name', 'owner')
    filter_horizontal = ('devices',)
    inlines = (DependencyInline,)


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('name', 'company', 'service', 'primary_device', 'criticality', 'is_active')
    list_filter = ('criticality', 'is_active', 'company')
    search_fields = ('name', 'company__name', 'service__name', 'primary_device__name')
    autocomplete_fields = ('service', 'primary_device')


@admin.register(AssetRelationship)
class AssetRelationshipAdmin(admin.ModelAdmin):
    list_display = ('source', 'relationship_type', 'target', 'impact_weight', 'is_active')
    list_filter = ('relationship_type', 'is_active')
    search_fields = ('source__name', 'target__name', 'label')
    autocomplete_fields = ('source', 'target')


@admin.register(Dependency)
class DependencyAdmin(admin.ModelAdmin):
    list_display = ('service', 'asset', 'is_required', 'impact_weight', 'is_active')
    list_filter = ('is_required', 'is_active', 'service__company')
    search_fields = ('service__name', 'asset__name', 'description')
    autocomplete_fields = ('service', 'asset')


@admin.register(BackupJob)
class BackupJobAdmin(admin.ModelAdmin):
    list_display = ('name', 'company', 'provider', 'last_status', 'last_run_at', 'is_active')
    list_filter = ('last_status', 'provider', 'is_active', 'company')
    search_fields = ('name', 'company__name', 'provider')
    filter_horizontal = ('protected_assets',)
