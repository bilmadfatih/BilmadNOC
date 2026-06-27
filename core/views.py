from django.db.models import Count, Q
from django.shortcuts import render

from core.models import Company, Location, Workspace
from monitoring.models import Device, Alert
from integrations.models import Integration


def _summary():
    devices = Device.objects.all()
    alerts = Alert.objects.filter(is_resolved=False)
    return {
        'company_count': Company.objects.filter(is_active=True).count(),
        'location_count': Location.objects.filter(is_active=True).count(),
        'device_count': devices.count(),
        'online_count': devices.filter(status='online').count(),
        'warning_count': devices.filter(status='warning').count(),
        'critical_count': devices.filter(status='critical').count(),
        'offline_count': devices.filter(status='offline').count(),
        'active_alert_count': alerts.count(),
        'critical_alert_count': alerts.filter(severity='critical').count(),
        'integration_count': Integration.objects.count(),
    }


def dashboard(request):
    company_rows = Company.objects.annotate(
        total_devices=Count('devices'),
        critical_devices=Count('devices', filter=Q(devices__status='critical')),
        offline_devices=Count('devices', filter=Q(devices__status='offline')),
        active_alerts=Count('alerts', filter=Q(alerts__is_resolved=False)),
    ).order_by('-active_alerts', 'name')[:8]
    recent_alerts = Alert.objects.select_related('company', 'device').filter(is_resolved=False)[:8]
    integrations = Integration.objects.select_related('company').all()[:8]
    return render(request, 'dashboard/home.html', {
        'summary': _summary(),
        'company_rows': company_rows,
        'recent_alerts': recent_alerts,
        'integrations': integrations,
    })


def noc_wall(request):
    return render(request, 'dashboard/noc_wall.html', {
        'summary': _summary(),
        'critical_alerts': Alert.objects.select_related('company', 'device').filter(is_resolved=False).order_by('-created_at')[:10],
        'companies': Company.objects.filter(is_active=True).order_by('name')[:12],
    })


def security_wall(request):
    security_devices = Device.objects.filter(device_type__in=['cctv_nvr', 'cctv_camera', 'alarm_panel'])
    return render(request, 'dashboard/security_wall.html', {
        'summary': _summary(),
        'camera_total': security_devices.filter(device_type='cctv_camera').count(),
        'camera_offline': security_devices.filter(device_type='cctv_camera', status='offline').count(),
        'nvr_total': security_devices.filter(device_type='cctv_nvr').count(),
        'alarm_panel_total': security_devices.filter(device_type='alarm_panel').count(),
        'security_alerts': Alert.objects.select_related('company', 'device').filter(is_resolved=False, device__device_type__in=['cctv_nvr', 'cctv_camera', 'alarm_panel'])[:10],
    })


def company_list(request):
    companies = Company.objects.all().order_by('name')
    return render(request, 'core/company_list.html', {'companies': companies})
