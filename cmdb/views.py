from django.shortcuts import render
from .models import Application, AssetRelationship, BackupJob, BusinessService, Dependency


def cmdb_overview(request):
    services = (
        BusinessService.objects
        .select_related('company')
        .prefetch_related('dependencies__asset', 'applications')
        .all()[:10]
    )
    relationships = AssetRelationship.objects.select_related('source', 'target').all()[:12]
    applications = Application.objects.select_related('company', 'service', 'primary_device').all()[:8]
    backup_jobs = BackupJob.objects.select_related('company').prefetch_related('protected_assets').all()[:8]
    dependencies = Dependency.objects.select_related('service', 'asset').all()[:12]

    return render(request, 'cmdb/overview.html', {
        'service_count': BusinessService.objects.count(),
        'application_count': Application.objects.count(),
        'relationship_count': AssetRelationship.objects.count(),
        'dependency_count': Dependency.objects.count(),
        'backup_job_count': BackupJob.objects.count(),
        'services': services,
        'relationships': relationships,
        'applications': applications,
        'backup_jobs': backup_jobs,
        'dependencies': dependencies,
    })
