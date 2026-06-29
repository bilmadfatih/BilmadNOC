from django.contrib import admin
from .models import MonitoringPlugin, PluginCheck, PluginResult


@admin.register(MonitoringPlugin)
class MonitoringPluginAdmin(admin.ModelAdmin):
    list_display = ("name", "plugin_type", "is_active")
    search_fields = ("name", "description")
    list_filter = ("plugin_type", "is_active")


@admin.register(PluginCheck)
class PluginCheckAdmin(admin.ModelAdmin):
    list_display = ("name", "asset", "plugin", "interval_seconds", "is_active")
    search_fields = ("name", "asset__name", "plugin__name")
    list_filter = ("plugin", "is_active")


@admin.register(PluginResult)
class PluginResultAdmin(admin.ModelAdmin):
    list_display = ("check", "success", "status", "response_time_ms", "created_at")
    search_fields = ("check__name", "message")
    list_filter = ("success", "status")
    readonly_fields = ("created_at", "updated_at")
