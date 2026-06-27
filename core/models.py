from django.db import models
from django.contrib.auth.models import User

class Company(models.Model):
    name = models.CharField('Firma Adı', max_length=200)
    short_name = models.CharField('Kısa Ad', max_length=80, blank=True)
    health_score = models.PositiveIntegerField('Sağlık Skoru', default=100)
    is_active = models.BooleanField('Aktif', default=True)
    notes = models.TextField('Notlar', blank=True)
    created_at = models.DateTimeField('Oluşturma', auto_now_add=True)

    class Meta:
        verbose_name = 'Firma'
        verbose_name_plural = 'Firmalar'
        ordering = ['name']

    def __str__(self):
        return self.name

class Location(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='locations', verbose_name='Firma')
    name = models.CharField('Lokasyon', max_length=150)
    address = models.TextField('Adres', blank=True)
    is_active = models.BooleanField('Aktif', default=True)

    class Meta:
        verbose_name = 'Lokasyon'
        verbose_name_plural = 'Lokasyonlar'
        ordering = ['company__name', 'name']

    def __str__(self):
        return f'{self.company.name} - {self.name}'

class Workspace(models.Model):
    WORKSPACE_TYPES = [
        ('noc', 'NOC Workspace'),
        ('it', 'IT Workspace'),
        ('network', 'Network Workspace'),
        ('cctv', 'CCTV Workspace'),
        ('alarm', 'Alarm Workspace'),
        ('executive', 'Yönetici Workspace'),
        ('partner', 'Partner Workspace'),
    ]
    name = models.CharField('Çalışma Alanı', max_length=150)
    workspace_type = models.CharField('Tip', max_length=30, choices=WORKSPACE_TYPES)
    users = models.ManyToManyField(User, blank=True, related_name='workspaces', verbose_name='Kullanıcılar')
    companies = models.ManyToManyField(Company, blank=True, related_name='workspaces', verbose_name='Firmalar')
    can_view_it = models.BooleanField(default=False)
    can_view_network = models.BooleanField(default=False)
    can_view_cctv = models.BooleanField(default=False)
    can_view_alarm = models.BooleanField(default=False)
    can_view_security = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Çalışma Alanı'
        verbose_name_plural = 'Çalışma Alanları'

    def __str__(self):
        return self.name
