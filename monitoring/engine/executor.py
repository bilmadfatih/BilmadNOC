from django.utils import timezone

from monitoring.models import Alert, CheckResult, Metric
from monitoring.plugins import get_plugin
from monitoring.services.asset_status import resolve_device_status


def execute_check(monitoring_check):
    plugin = get_plugin(monitoring_check.check_type)
    if plugin is None:
        success = False
        status = 'offline'
        response_time = None
        message = f'Desteklenmeyen plugin tipi: {monitoring_check.check_type}'
        raw = {'check_type': monitoring_check.check_type}
    else:
        plugin_result = plugin.run(monitoring_check)
        success = plugin_result.success
        status = plugin_result.status
        response_time = plugin_result.response_time_ms
        message = plugin_result.message
        raw = plugin_result.raw_data

    device = monitoring_check.device
    if not success and device.is_critical:
        status = 'critical'

    result = CheckResult.objects.create(
        monitoring_check=monitoring_check,
        device=device,
        success=success,
        status=status,
        response_time_ms=response_time,
        message=message,
        raw_data=raw,
    )

    now = timezone.now()
    monitoring_check.last_run_at = now
    monitoring_check.save(update_fields=['last_run_at'])

    device.status = resolve_device_status(device, current_result=result)
    device.last_checked_at = now
    device.last_error = '' if success else message
    device.save(update_fields=['status', 'last_checked_at', 'last_error'])

    if response_time is not None:
        Metric.objects.create(device=device, name=f'{monitoring_check.check_type}_response_time', value=response_time, unit='ms')

    title = f'{device.name} {monitoring_check.get_check_type_display()} başarısız'
    if not success:
        Alert.objects.get_or_create(
            company=device.company,
            device=device,
            title=title,
            is_resolved=False,
            defaults={'message': message, 'severity': 'critical' if device.is_critical else 'warning'},
        )
    else:
        Alert.objects.filter(device=device, title=title, is_resolved=False).update(is_resolved=True)

    return result
