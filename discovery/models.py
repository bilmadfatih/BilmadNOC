from django.db import models
from django.utils import timezone

from core.models import Company, Location
from monitoring.models import Device


class DiscoveryRun(models.Model):
    STATUS = [
        ('pending', 'Bekliyor'),
        ('running', 'Çalışıyor'),
        ('completed', 'Tamamlandı'),
        ('failed', 'Hata'),
    ]

    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='discovery_runs', verbose_name='Firma')
    location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True, blank=True, related_name='discovery_runs', verbose_name='Lokasyon')
    cidr = models.CharField('IP Aralığı', max_length=64)
    status = models.CharField('Durum', max_length=20, choices=STATUS, default='pending')
    scan_ping = models.BooleanField('Ping', default=True)
    scan_tcp = models.BooleanField('TCP', default=True)
    started_at = models.DateTimeField('Başlama', null=True, blank=True)
    finished_at = models.DateTimeField('Bitiş', null=True, blank=True)
    error_message = models.TextField('Hata', blank=True)
    created_at = models.DateTimeField('Oluşturma', auto_now_add=True)

    class Meta:
        verbose_name = 'Keşif Taraması'
        verbose_name_plural = 'Keşif Taramaları'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.company.name} - {self.cidr}'

    @property
    def found_count(self):
        return self.hosts.count()

    @property
    def imported_count(self):
        return self.hosts.filter(imported_device__isnull=False).count()

    def mark_running(self):
        self.status = 'running'
        self.started_at = timezone.now()
        self.save(update_fields=['status', 'started_at'])

    def mark_completed(self):
        self.status = 'completed'
        self.finished_at = timezone.now()
        self.save(update_fields=['status', 'finished_at'])

    def mark_failed(self, message):
        self.status = 'failed'
        self.error_message = str(message)
        self.finished_at = timezone.now()
        self.save(update_fields=['status', 'error_message', 'finished_at'])


class DiscoveryHost(models.Model):
    DEVICE_TYPES = Device.DEVICE_TYPES

    discovery_run = models.ForeignKey(DiscoveryRun, on_delete=models.CASCADE, related_name='hosts')
    ip_address = models.GenericIPAddressField('IP Adresi')
    hostname = models.CharField('Hostname', max_length=150, blank=True)
    suggested_name = models.CharField('Önerilen Ad', max_length=180, blank=True)
    suggested_type = models.CharField('Önerilen Tip', max_length=40, choices=DEVICE_TYPES, default='other')
    open_ports = models.JSONField('Açık Portlar', default=list, blank=True)
    confidence = models.PositiveIntegerField('Güven', default=50)
    imported_device = models.ForeignKey(Device, on_delete=models.SET_NULL, null=True, blank=True, related_name='discovery_sources')
    created_at = models.DateTimeField('Oluşturma', auto_now_add=True)

    class Meta:
        verbose_name = 'Keşfedilen Host'
        verbose_name_plural = 'Keşfedilen Hostlar'
        ordering = ['ip_address']
        unique_together = [('discovery_run', 'ip_address')]

    def __str__(self):
        return f'{self.ip_address} - {self.suggested_name or self.hostname or self.suggested_type}'
