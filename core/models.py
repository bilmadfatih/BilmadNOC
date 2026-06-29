import uuid
from django.conf import settings
from django.db import models


# -----------------------------------------------------------------------------
# Legacy v0.3 models
# -----------------------------------------------------------------------------
# Bu sınıflar mevcut veritabanındaki core_company, core_location ve
# core_workspace tablolarıyla uyumludur. Sprint 3.2 Discovery Engine bu sağlam
# baseline üzerine kurulmuştur.


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
    users = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='workspaces', verbose_name='Kullanıcılar')
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


# -----------------------------------------------------------------------------
# Sprint 3 compatibility base models
# -----------------------------------------------------------------------------
# Yeni CMDB / multi-tenant mimariye geçiş için bırakılmış uyumlu temel sınıflar.
# Eski ekranlar Company/Location üzerinden çalışmaya devam eder.


class ActiveManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_deleted=False)


class BaseModel(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, db_index=True)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='created_%(class)s_set',
    )
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='updated_%(class)s_set',
    )

    objects = ActiveManager()
    all_objects = models.Manager()

    class Meta:
        abstract = True

    def delete(self, using=None, keep_parents=False):
        self.is_deleted = True
        self.is_active = False
        self.save(update_fields=['is_deleted', 'is_active', 'updated_at'])


class Tenant(BaseModel):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Customer(BaseModel):
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name='customers', null=True, blank=True)
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=50, unique=True)
    tax_number = models.CharField(max_length=50, blank=True, null=True)
    contact_name = models.CharField(max_length=255, blank=True, null=True)
    contact_email = models.EmailField(blank=True, null=True)
    contact_phone = models.CharField(max_length=50, blank=True, null=True)
    address = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Site(BaseModel):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='sites')
    name = models.CharField(max_length=255)
    site_type = models.CharField(max_length=100, default='branch')
    address = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ['customer__name', 'name']

    def __str__(self):
        return f'{self.customer.name} - {self.name}'


class AuditLog(models.Model):
    ACTION_CHOICES = (
        ('create', 'Create'),
        ('update', 'Update'),
        ('delete', 'Delete'),
        ('system', 'System'),
    )

    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, db_index=True)
    action = models.CharField(max_length=30, choices=ACTION_CHOICES)
    model_name = models.CharField(max_length=100)
    object_uuid = models.UUIDField(null=True, blank=True)
    message = models.TextField()
    old_value = models.JSONField(default=dict, blank=True)
    new_value = models.JSONField(default=dict, blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.action} - {self.model_name} - {self.created_at}'
