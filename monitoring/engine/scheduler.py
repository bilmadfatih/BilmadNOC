from django.utils import timezone

from monitoring.engine.dispatcher import dispatch_check
from monitoring.models import MonitoringCheck


def due_checks(limit=100):
    now = timezone.now()
    checks = []
    for monitoring_check in MonitoringCheck.objects.select_related('device', 'device__company').filter(status='enabled')[:limit]:
        if monitoring_check.last_run_at is None:
            checks.append(monitoring_check)
            continue
        elapsed = (now - monitoring_check.last_run_at).total_seconds()
        if elapsed >= monitoring_check.interval_seconds:
            checks.append(monitoring_check)
    return checks


def run_due_checks(limit=100):
    results = []
    for monitoring_check in due_checks(limit=limit):
        results.append(dispatch_check(monitoring_check))
    return results
