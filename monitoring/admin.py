from django.contrib import admin
from .models import Alert, CheckResult, Device, Metric, MonitoringCheck


@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    list_display = ('name', 'company', 'location', 'device_type', 'ip_address', 'status', 'is_critical', 'last_checked_at')
    list_filter = ('status', 'device_type', 'is_critical', 'company')
    search_fields = ('name', 'hostname', 'ip_address', 'company__name', 'vendor', 'model')


@admin.register(Metric)
class MetricAdmin(admin.ModelAdmin):
    list_display = ('device', 'name', 'value', 'unit', 'collected_at')
    list_filter = ('name', 'device__company')
    search_fields = ('device__name', 'name')


@admin.register(Alert)
class AlertAdmin(admin.ModelAdmin):
    list_display = ('title', 'company', 'device', 'severity', 'is_resolved', 'created_at')
    list_filter = ('severity', 'is_resolved', 'company')
    search_fields = ('title', 'message', 'company__name', 'device__name')


@admin.register(MonitoringCheck)
class MonitoringCheckAdmin(admin.ModelAdmin):
    list_display = ('device', 'check_type', 'name', 'target', 'port', 'status', 'interval_seconds', 'last_run_at')
    list_filter = ('check_type', 'status', 'device__company')
    search_fields = ('device__name', 'target', 'name')


@admin.register(CheckResult)
class CheckResultAdmin(admin.ModelAdmin):
    list_display = ('device', 'monitoring_check', 'success', 'status', 'response_time_ms', 'checked_at')
    list_filter = ('success', 'status', 'monitoring_check__check_type', 'device__company')
    search_fields = ('device__name', 'message')
    readonly_fields = ('raw_data',)
