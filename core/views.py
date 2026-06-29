from django.db.models import Count, Q
from django.shortcuts import get_object_or_404, redirect, render

from core.models import Company, Location, Workspace
from monitoring.models import Device, Alert, Metric, CheckResult, MonitoringCheck
from integrations.models import Integration
from monitoring.services.checks import ensure_default_checks, run_device_checks
from monitoring.services.health import calculate_asset_health, score_class


DEVICE_ICON_MAP = {
    'server': '🖥️',
    'vmware': '☁️',
    'switch': '🔀',
    'access_point': '📶',
    'firewall': '🛡️',
    'router': '🌐',
    'backup': '💾',
    'sensway': '🌡️',
    'cctv_nvr': '🎥',
    'cctv_camera': '📷',
    'alarm_panel': '🚨',
    'm365': '☁️',
    'security': '🔐',
    'other': '📦',
}


def _device_icon(device):
    return DEVICE_ICON_MAP.get(getattr(device, 'device_type', ''), '📦')


def _result_stats(results):
    rows = list(results)
    total = len(rows)
    ok = len([r for r in rows if r.success])
    fail = total - ok
    times = [r.response_time_ms for r in rows if r.response_time_ms is not None]
    avg_ms = round(sum(times) / len(times)) if times else None
    uptime = round((ok / total) * 100) if total else None
    return {
        'total': total,
        'ok': ok,
        'fail': fail,
        'avg_ms': avg_ms,
        'uptime': uptime,
    }


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
        'check_count': MonitoringCheck.objects.filter(status='enabled').count(),
        'last_check_count': CheckResult.objects.count(),
        'last_check_at': CheckResult.objects.order_by('-checked_at').values_list('checked_at', flat=True).first(),
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
    latest_checks = CheckResult.objects.select_related('device', 'monitoring_check', 'device__company')[:10]
    return render(request, 'dashboard/home.html', {
        'summary': _summary(),
        'company_rows': company_rows,
        'recent_alerts': recent_alerts,
        'integrations': integrations,
        'latest_checks': latest_checks,
    })


def noc_wall(request):
    return render(request, 'dashboard/noc_wall.html', {
        'summary': _summary(),
        'critical_alerts': Alert.objects.select_related('company', 'device').filter(is_resolved=False).order_by('-created_at')[:10],
        'companies': Company.objects.filter(is_active=True).order_by('name')[:12],
        'latest_checks': CheckResult.objects.select_related('device', 'monitoring_check')[:12],
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
    return render(request, 'core/company_list.html', {'summary': _summary(), 'companies': companies})


def company_detail(request, pk):
    company = get_object_or_404(Company, pk=pk)
    assets = Device.objects.select_related('company', 'location').filter(company=company).order_by('name')
    alerts = Alert.objects.select_related('device').filter(company=company, is_resolved=False)[:10]
    return render(request, 'core/company_detail.html', {
        'summary': _summary(),
        'company': company,
        'assets': assets,
        'alerts': alerts,
        'locations': Location.objects.filter(company=company, is_active=True),
        'integrations': Integration.objects.filter(company=company),
        'asset_count': assets.count(),
        'active_alert_count': alerts.count(),
        'critical_count': assets.filter(status='critical').count(),
        'offline_count': assets.filter(status='offline').count(),
    })


def asset_list(request):
    q = request.GET.get('q', '').strip()
    status = request.GET.get('status', '').strip()
    device_type = request.GET.get('type', '').strip()

    assets = Device.objects.select_related('company', 'location').all().order_by('company__name', 'name')
    if q:
        assets = assets.filter(
            Q(name__icontains=q)
            | Q(ip_address__icontains=q)
            | Q(hostname__icontains=q)
            | Q(vendor__icontains=q)
            | Q(model__icontains=q)
            | Q(company__name__icontains=q)
        )
    if status:
        assets = assets.filter(status=status)
    if device_type:
        assets = assets.filter(device_type=device_type)

    for asset in assets:
        asset.health_score, asset.health_reasons = calculate_asset_health(asset)
        asset.health_class = score_class(asset.health_score)
        asset.device_icon = _device_icon(asset)

    return render(request, 'assets/list.html', {
        'summary': _summary(),
        'assets': assets,
        'q': q,
        'status': status,
        'device_type': device_type,
        'status_choices': Device.STATUS,
        'type_choices': Device.DEVICE_TYPES,
    })


def _asset_health_score(asset):
    score, _reasons = calculate_asset_health(asset)
    return score


def asset_detail(request, pk):
    asset = get_object_or_404(Device.objects.select_related('company', 'location'), pk=pk)
    ensure_default_checks(asset)
    checks = MonitoringCheck.objects.filter(device=asset).order_by('check_type', 'name')
    latest_results = CheckResult.objects.select_related('monitoring_check').filter(device=asset)[:30]
    latest_results_list = list(latest_results)
    latest_result = latest_results_list[0] if latest_results_list else None
    health_score, health_reasons = calculate_asset_health(asset)
    plugin_summary = []
    for check in checks:
        last_result = check.results.first()
        plugin_summary.append({'check': check, 'last_result': last_result})
    open_alerts = Alert.objects.filter(device=asset, is_resolved=False).order_by('-created_at')
    result_stats = _result_stats(latest_results_list)
    recent_success = list(reversed(latest_results_list[:16]))
    response_metrics = Metric.objects.filter(device=asset, name__icontains='response_time')[:20]
    return render(request, 'assets/detail.html', {
        'summary': _summary(),
        'asset': asset,
        'asset_icon': _device_icon(asset),
        'health_score': health_score,
        'health_reasons': health_reasons,
        'health_class': score_class(health_score),
        'plugin_summary': plugin_summary,
        'latest_result': latest_result,
        'metrics': Metric.objects.filter(device=asset)[:20],
        'response_metrics': response_metrics,
        'result_stats': result_stats,
        'recent_success': recent_success,
        'alerts': open_alerts[:10],
        'open_alert_count': open_alerts.count(),
        'checks': checks,
        'latest_results': latest_results_list,
        'latest_results_count': len(latest_results_list),
    })


def asset_run_checks(request, pk):
    asset = get_object_or_404(Device, pk=pk)
    run_device_checks(asset)
    return redirect('asset_detail', pk=asset.pk)


def integration_list(request):
    return render(request, 'integrations/list.html', {
        'summary': _summary(),
        'integrations': Integration.objects.select_related('company').all().order_by('company__name', 'name'),
    })
