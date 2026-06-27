from django.db import models
from core.models import Company


class Integration(models.Model):
    INTEGRATION_TYPES = [
        ('berqnet', 'Berqnet SASE'),
        ('vmware', 'VMware ESXi / vCenter'),
        ('narbulut', 'Narbulut Backup'),
        ('sensway', 'Sensway Ortam İzleme'),
        ('bitdefender', 'Bitdefender GravityZone'),
        ('m365', 'Microsoft 365'),
        ('cctv', 'CCTV / NVR'),
        ('alarm', 'Alarm Sistemi'),
        ('snmp', 'SNMP Network'),
        ('other', 'Diğer'),
    ]
    STATUS = [
        ('not_configured', 'Yapılandırılmadı'),
        ('connected', 'Bağlı'),
        ('error', 'Hata'),
        ('disabled', 'Pasif'),
    ]

    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='integrations', verbose_name='Firma')
    name = models.CharField('Entegrasyon Adı', max_length=150)
    integration_type = models.CharField('Tip', max_length=40, choices=INTEGRATION_TYPES)
    status = models.CharField('Durum', max_length=30, choices=STATUS, default='not_configured')
    base_url = models.URLField('API / Panel URL', blank=True)
    username = models.CharField('Kullanıcı Adı', max_length=150, blank=True)
    notes = models.TextField('Notlar', blank=True)
    last_sync_at = models.DateTimeField('Son Senkronizasyon', null=True, blank=True)
    is_active = models.BooleanField('Aktif', default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Entegrasyon'
        verbose_name_plural = 'Entegrasyonlar'
        ordering = ['company__name', 'name']

    def __str__(self):
        return f'{self.company.name} - {self.name}'
