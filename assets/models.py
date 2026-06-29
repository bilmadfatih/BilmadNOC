from django.db import models
from core.models import BaseModel, Customer, Site


class AssetType(models.TextChoices):
    SERVER = "server", "Server"
    FIREWALL = "firewall", "Firewall"
    SWITCH = "switch", "Switch"
    ROUTER = "router", "Router"
    NAS = "nas", "NAS"
    ACCESS_POINT = "access_point", "Access Point"
    PRINTER = "printer", "Printer"
    UPS = "ups", "UPS"
    CAMERA = "camera", "Camera"
    VM = "vm", "Virtual Machine"
    HYPERVISOR = "hypervisor", "Hypervisor"
    OTHER = "other", "Other"


class AssetStatus(models.TextChoices):
    ONLINE = "online", "Online"
    WARNING = "warning", "Warning"
    CRITICAL = "critical", "Critical"
    OFFLINE = "offline", "Offline"
    UNKNOWN = "unknown", "Unknown"


class Manufacturer(BaseModel):
    name = models.CharField(max_length=120, unique=True)

    def __str__(self):
        return self.name


class Location(BaseModel):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="locations")
    site = models.ForeignKey(Site, on_delete=models.CASCADE, related_name="locations", null=True, blank=True)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.customer.name} - {self.name}"


class Asset(BaseModel):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="assets")
    site = models.ForeignKey(Site, on_delete=models.SET_NULL, blank=True, null=True, related_name="assets")
    location = models.ForeignKey(Location, on_delete=models.SET_NULL, blank=True, null=True, related_name="assets")
    manufacturer = models.ForeignKey(Manufacturer, on_delete=models.SET_NULL, blank=True, null=True)

    name = models.CharField(max_length=255)
    asset_type = models.CharField(max_length=50, choices=AssetType.choices, default=AssetType.OTHER)
    status = models.CharField(max_length=50, choices=AssetStatus.choices, default=AssetStatus.UNKNOWN)

    ip_address = models.GenericIPAddressField(blank=True, null=True)
    hostname = models.CharField(max_length=255, blank=True, null=True)
    model = models.CharField(max_length=100, blank=True, null=True)
    serial_number = models.CharField(max_length=100, blank=True, null=True)
    os_name = models.CharField(max_length=100, blank=True, null=True)
    os_version = models.CharField(max_length=100, blank=True, null=True)

    monitoring_enabled = models.BooleanField(default=True)
    last_seen_at = models.DateTimeField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ["customer__name", "name"]
        indexes = [
            models.Index(fields=["asset_type", "status"]),
            models.Index(fields=["ip_address"]),
        ]

    def __str__(self):
        return f"{self.name} ({self.ip_address or 'no-ip'})"


class AssetMetric(BaseModel):
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE, related_name="metrics")
    key = models.CharField(max_length=100)
    value = models.CharField(max_length=255)
    unit = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.asset.name} - {self.key}: {self.value}"
