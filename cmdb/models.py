from django.db import models
from django.utils.translation import gettext_lazy as _

from core.models import BaseModel, Company
from monitoring.models import Device


class ServiceCriticality(models.TextChoices):
    LOW = 'low', _('Low')
    MEDIUM = 'medium', _('Medium')
    HIGH = 'high', _('High')
    CRITICAL = 'critical', _('Critical')


class RelationshipType(models.TextChoices):
    DEPENDS_ON = 'depends_on', _('Depends on')
    HOSTS = 'hosts', _('Hosts')
    RUNS_ON = 'runs_on', _('Runs on')
    CONNECTED_TO = 'connected_to', _('Connected to')
    BACKED_UP_BY = 'backed_up_by', _('Backed up by')
    PROTECTS = 'protects', _('Protects')
    POWERS = 'powers', _('Powers')
    MONITORS = 'monitors', _('Monitors')
    RELATED = 'related', _('Related')


class BusinessService(BaseModel):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='business_services', verbose_name=_('Customer'))
    name = models.CharField(_('Service Name'), max_length=160)
    owner = models.CharField(_('Owner'), max_length=120, blank=True)
    criticality = models.CharField(_('Criticality'), max_length=20, choices=ServiceCriticality.choices, default=ServiceCriticality.MEDIUM)
    description = models.TextField(_('Description'), blank=True)
    devices = models.ManyToManyField(Device, blank=True, related_name='business_services', verbose_name=_('Related Assets'))

    class Meta:
        verbose_name = _('Business Service')
        verbose_name_plural = _('Business Services')
        ordering = ['company__name', 'name']
        indexes = [models.Index(fields=['company', 'criticality'])]

    def __str__(self):
        return f'{self.company.name} - {self.name}'


class Application(BaseModel):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='applications', verbose_name=_('Customer'))
    name = models.CharField(_('Application Name'), max_length=160)
    service = models.ForeignKey(BusinessService, on_delete=models.SET_NULL, null=True, blank=True, related_name='applications', verbose_name=_('Business Service'))
    primary_device = models.ForeignKey(Device, on_delete=models.SET_NULL, null=True, blank=True, related_name='primary_applications', verbose_name=_('Primary Asset'))
    url = models.URLField(_('URL'), blank=True)
    criticality = models.CharField(_('Criticality'), max_length=20, choices=ServiceCriticality.choices, default=ServiceCriticality.MEDIUM)
    description = models.TextField(_('Description'), blank=True)

    class Meta:
        verbose_name = _('Application')
        verbose_name_plural = _('Applications')
        ordering = ['company__name', 'name']

    def __str__(self):
        return f'{self.company.name} - {self.name}'


class AssetRelationship(BaseModel):
    source = models.ForeignKey(Device, on_delete=models.CASCADE, related_name='outgoing_relationships', verbose_name=_('Source Asset'))
    target = models.ForeignKey(Device, on_delete=models.CASCADE, related_name='incoming_relationships', verbose_name=_('Target Asset'))
    relationship_type = models.CharField(_('Relationship Type'), max_length=30, choices=RelationshipType.choices, default=RelationshipType.RELATED)
    label = models.CharField(_('Label'), max_length=120, blank=True)
    impact_weight = models.PositiveSmallIntegerField(_('Impact Weight'), default=50, help_text=_('0-100 impact score used by root cause analysis.'))
    notes = models.TextField(_('Notes'), blank=True)

    class Meta:
        verbose_name = _('Asset Relationship')
        verbose_name_plural = _('Asset Relationships')
        ordering = ['source__company__name', 'source__name', 'relationship_type']
        constraints = [
            models.UniqueConstraint(fields=['source', 'target', 'relationship_type'], name='uniq_cmdb_asset_relationship')
        ]
        indexes = [models.Index(fields=['relationship_type'])]

    def __str__(self):
        return f'{self.source.name} -> {self.get_relationship_type_display()} -> {self.target.name}'


class Dependency(BaseModel):
    service = models.ForeignKey(BusinessService, on_delete=models.CASCADE, related_name='dependencies', verbose_name=_('Business Service'))
    asset = models.ForeignKey(Device, on_delete=models.CASCADE, related_name='service_dependencies', verbose_name=_('Asset'))
    description = models.CharField(_('Description'), max_length=255, blank=True)
    is_required = models.BooleanField(_('Required'), default=True)
    impact_weight = models.PositiveSmallIntegerField(_('Impact Weight'), default=50)

    class Meta:
        verbose_name = _('Service Dependency')
        verbose_name_plural = _('Service Dependencies')
        ordering = ['service__company__name', 'service__name', 'asset__name']
        constraints = [
            models.UniqueConstraint(fields=['service', 'asset'], name='uniq_cmdb_service_asset_dependency')
        ]

    def __str__(self):
        return f'{self.service.name} depends on {self.asset.name}'


class BackupJob(BaseModel):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='backup_jobs', verbose_name=_('Customer'))
    name = models.CharField(_('Backup Job'), max_length=160)
    protected_assets = models.ManyToManyField(Device, blank=True, related_name='backup_jobs', verbose_name=_('Protected Assets'))
    provider = models.CharField(_('Provider'), max_length=80, blank=True)
    schedule = models.CharField(_('Schedule'), max_length=120, blank=True)
    last_status = models.CharField(_('Last Status'), max_length=30, default='unknown')
    last_run_at = models.DateTimeField(_('Last Run'), null=True, blank=True)
    notes = models.TextField(_('Notes'), blank=True)

    class Meta:
        verbose_name = _('Backup Job')
        verbose_name_plural = _('Backup Jobs')
        ordering = ['company__name', 'name']

    def __str__(self):
        return f'{self.company.name} - {self.name}'
