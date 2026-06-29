from django.contrib import admin

from .models import DiscoveryRun, DiscoveryHost


class DiscoveryHostInline(admin.TabularInline):
    model = DiscoveryHost
    extra = 0
    readonly_fields = ('ip_address', 'hostname', 'suggested_name', 'suggested_type', 'open_ports', 'confidence', 'imported_device', 'created_at')
    can_delete = False


@admin.register(DiscoveryRun)
class DiscoveryRunAdmin(admin.ModelAdmin):
    list_display = ('company', 'location', 'cidr', 'status', 'found_count', 'imported_count', 'created_at')
    list_filter = ('status', 'company')
    search_fields = ('cidr', 'company__name', 'location__name')
    inlines = [DiscoveryHostInline]


@admin.register(DiscoveryHost)
class DiscoveryHostAdmin(admin.ModelAdmin):
    list_display = ('ip_address', 'suggested_name', 'suggested_type', 'confidence', 'imported_device', 'discovery_run')
    list_filter = ('suggested_type',)
    search_fields = ('ip_address', 'hostname', 'suggested_name')
