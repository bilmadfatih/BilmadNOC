from monitoring.engine.executor import execute_check
from monitoring.models import MonitoringCheck
from monitoring.services.provisioning import ensure_default_checks


def dispatch_check(monitoring_check):
    return execute_check(monitoring_check)


def dispatch_device(device):
    ensure_default_checks(device)
    results = []
    for monitoring_check in device.checks.filter(status='enabled').order_by('check_type', 'name'):
        results.append(dispatch_check(monitoring_check))
    return results


def dispatch_all_enabled():
    results = []
    for monitoring_check in MonitoringCheck.objects.select_related('device', 'device__company').filter(status='enabled'):
        results.append(dispatch_check(monitoring_check))
    return results
