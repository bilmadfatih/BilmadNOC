from django.contrib import admin
from .models import Device, Metric, Alert


@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    list_display = ('company', 'location', 'name', 'device_type', 'vendor', 'ip_address', 'status', 'is_critical')
    list_filter = ('company', 'location', 'device_type', 'status', 'is_critical', 'vendor')
    search_fields = ('name', 'ip_address', 'hostname', 'vendor', 'model')


@admin.register(Metric)
class MetricAdmin(admin.ModelAdmin):
    list_display = ('device', 'name', 'value', 'unit', 'collected_at')
    list_filter = ('name', 'unit')
    search_fields = ('device__name', 'name')


@admin.register(Alert)
class AlertAdmin(admin.ModelAdmin):
    list_display = ('company', 'device', 'title', 'severity', 'is_resolved', 'created_at')
    list_filter = ('severity', 'is_resolved', 'company')
    search_fields = ('title', 'message', 'company__name', 'device__name')
