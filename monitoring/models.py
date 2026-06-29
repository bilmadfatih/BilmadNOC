from django.db import models
from core.models import Company, Location

class Device(models.Model):
    DEVICE_TYPES = [
        ('server', 'Sunucu'), ('vmware', 'VMware ESXi'), ('switch', 'Switch'),
        ('access_point', 'Access Point'), ('firewall', 'Firewall'), ('router', 'Router'),
        ('backup', 'Backup Sistemi'), ('sensway', 'Ortam Sensörü'), ('cctv_nvr', 'NVR/DVR'),
        ('cctv_camera', 'Kamera'), ('alarm_panel', 'Alarm Paneli'), ('m365', 'Microsoft 365'),
        ('security', 'Güvenlik Sistemi'), ('other', 'Diğer')]
    STATUS = [('unknown', 'Bilinmiyor'), ('online', 'Online'), ('offline', 'Offline'), ('warning', 'Uyarı'), ('critical', 'Kritik')]
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='devices', verbose_name='Firma')
    location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True, blank=True, related_name='devices', verbose_name='Lokasyon')
    name = models.CharField('Cihaz Adı', max_length=150)
    device_type = models.CharField('Cihaz Tipi', max_length=40, choices=DEVICE_TYPES)
    vendor = models.CharField('Marka', max_length=80, blank=True)
    model = models.CharField('Model', max_length=100, blank=True)
    ip_address = models.GenericIPAddressField('IP Adresi', null=True, blank=True)
    hostname = models.CharField('Hostname', max_length=150, blank=True)
    is_critical = models.BooleanField('Kritik Cihaz', default=False)
    status = models.CharField('Durum', max_length=20, choices=STATUS, default='unknown')
    last_checked_at = models.DateTimeField('Son Kontrol', null=True, blank=True)
    last_error = models.TextField('Son Hata', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Cihaz'
        verbose_name_plural = 'Cihazlar'
        ordering = ['company__name', 'name']

    def __str__(self):
        return f'{self.company.name} - {self.name}'

class Metric(models.Model):
    device = models.ForeignKey(Device, on_delete=models.CASCADE, related_name='metrics')
    name = models.CharField(max_length=100)
    value = models.FloatField(null=True, blank=True)
    unit = models.CharField(max_length=30, blank=True)
    collected_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Metrik'
        verbose_name_plural = 'Metrikler'
        ordering = ['-collected_at']

class Alert(models.Model):
    SEVERITIES = [('info', 'Bilgi'), ('warning', 'Uyarı'), ('critical', 'Kritik')]
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='alerts')
    device = models.ForeignKey(Device, on_delete=models.SET_NULL, null=True, blank=True, related_name='alerts')
    title = models.CharField('Başlık', max_length=200)
    message = models.TextField('Açıklama', blank=True)
    severity = models.CharField('Seviye', max_length=20, choices=SEVERITIES, default='warning')
    is_resolved = models.BooleanField('Çözüldü', default=False)
    created_at = models.DateTimeField('Oluşturma', auto_now_add=True)

    class Meta:
        verbose_name = 'Alarm'
        verbose_name_plural = 'Alarmlar'
        ordering = ['-created_at']

    def __str__(self):
        return self.title

class MonitoringCheck(models.Model):
    CHECK_TYPES = [
        ('ping', 'Ping'),
        ('http', 'HTTP'),
        ('tcp', 'TCP Port'),
    ]
    STATUS = [
        ('enabled', 'Aktif'),
        ('disabled', 'Pasif'),
    ]

    device = models.ForeignKey(Device, on_delete=models.CASCADE, related_name='checks', verbose_name='Cihaz')
    check_type = models.CharField('Check Tipi', max_length=20, choices=CHECK_TYPES, default='ping')
    name = models.CharField('Check Adı', max_length=120, blank=True)
    target = models.CharField('Hedef', max_length=255, blank=True)
    port = models.PositiveIntegerField('Port', null=True, blank=True)
    path = models.CharField('Path', max_length=255, blank=True, default='/')
    interval_seconds = models.PositiveIntegerField('Periyot', default=60)
    timeout_seconds = models.PositiveIntegerField('Timeout', default=3)
    status = models.CharField('Durum', max_length=20, choices=STATUS, default='enabled')
    last_run_at = models.DateTimeField('Son Çalışma', null=True, blank=True)
    created_at = models.DateTimeField('Oluşturma', auto_now_add=True)

    class Meta:
        verbose_name = 'Monitoring Check'
        verbose_name_plural = 'Monitoring Checks'
        ordering = ['device__company__name', 'device__name', 'check_type']

    def __str__(self):
        label = self.name or self.get_check_type_display()
        return f'{self.device.name} - {label}'

    @property
    def effective_target(self):
        return self.target or self.device.ip_address or self.device.hostname or ''


class CheckResult(models.Model):
    monitoring_check = models.ForeignKey(MonitoringCheck, on_delete=models.CASCADE, related_name='results', verbose_name='Monitoring Check')
    device = models.ForeignKey(Device, on_delete=models.CASCADE, related_name='check_results')
    success = models.BooleanField('Başarılı', default=False)
    status = models.CharField('Sonuç', max_length=20, default='unknown')
    response_time_ms = models.PositiveIntegerField('Yanıt Süresi ms', null=True, blank=True)
    message = models.TextField('Mesaj', blank=True)
    raw_data = models.JSONField('Ham Veri', default=dict, blank=True)
    checked_at = models.DateTimeField('Kontrol Zamanı', auto_now_add=True)

    class Meta:
        verbose_name = 'Check Result'
        verbose_name_plural = 'Check Results'
        ordering = ['-checked_at']
        indexes = [
            models.Index(fields=['device', '-checked_at']),
            models.Index(fields=['monitoring_check', '-checked_at']),
            models.Index(fields=['success', '-checked_at']),
        ]

    def __str__(self):
        return f'{self.device.name} - {self.status} - {self.checked_at}'
