from django.db import models
from core.models import BaseModel
from assets.models import Asset


class PluginType(models.TextChoices):
    PING = "ping", "Ping"
    HTTP = "http", "HTTP"
    TCP_PORT = "tcp_port", "TCP Port"
    DNS = "dns", "DNS"
    SMTP = "smtp", "SMTP"
    SNMP = "snmp", "SNMP"
    CUSTOM = "custom", "Custom"


class MonitoringPlugin(BaseModel):
    name = models.CharField(max_length=100, unique=True)
    plugin_type = models.CharField(max_length=50, choices=PluginType.choices)
    description = models.TextField(blank=True, null=True)
    default_config = models.JSONField(default=dict, blank=True)

    def __str__(self):
        return self.name


class PluginCheck(BaseModel):
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE, related_name="checks")
    plugin = models.ForeignKey(MonitoringPlugin, on_delete=models.CASCADE, related_name="checks")
    name = models.CharField(max_length=150)
    interval_seconds = models.PositiveIntegerField(default=60)
    timeout_seconds = models.PositiveIntegerField(default=5)
    config = models.JSONField(default=dict, blank=True)
    last_run_at = models.DateTimeField(blank=True, null=True)
    next_run_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        ordering = ["asset__name", "name"]

    def __str__(self):
        return f"{self.asset.name} - {self.name}"


class PluginResult(BaseModel):
    check = models.ForeignKey(PluginCheck, on_delete=models.CASCADE, related_name="results")
    success = models.BooleanField(default=False)
    status = models.CharField(max_length=50, default="unknown")
    message = models.TextField(blank=True, null=True)
    response_time_ms = models.PositiveIntegerField(blank=True, null=True)
    raw_data = models.JSONField(default=dict, blank=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["success", "status"]),
            models.Index(fields=["created_at"]),
        ]

    def __str__(self):
        return f"{self.check} - {self.status}"
