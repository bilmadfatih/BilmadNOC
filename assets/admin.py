from django.contrib import admin
from .models import Asset, AssetMetric, Location, Manufacturer


@admin.register(Manufacturer)
class ManufacturerAdmin(admin.ModelAdmin):
    list_display = ("name", "is_active")
    search_fields = ("name",)


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ("name", "customer", "site", "is_active")
    search_fields = ("name", "customer__name", "site__name")
    list_filter = ("customer", "is_active")


@admin.register(Asset)
class AssetAdmin(admin.ModelAdmin):
    list_display = ("name", "customer", "asset_type", "ip_address", "status", "monitoring_enabled")
    search_fields = ("name", "ip_address", "hostname", "serial_number", "customer__name")
    list_filter = ("asset_type", "status", "monitoring_enabled", "customer")


@admin.register(AssetMetric)
class AssetMetricAdmin(admin.ModelAdmin):
    list_display = ("asset", "key", "value", "unit", "created_at")
    search_fields = ("asset__name", "key", "value")
    list_filter = ("key",)
