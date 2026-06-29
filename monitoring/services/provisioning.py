from monitoring.models import MonitoringCheck


def ensure_default_checks(device):
    if device.ip_address and not device.checks.filter(check_type='ping').exists():
        MonitoringCheck.objects.create(
            device=device,
            check_type='ping',
            name='Default Ping',
            target=str(device.ip_address),
            interval_seconds=60,
        )
    if device.ip_address and device.device_type in ('server', 'vmware', 'firewall', 'router') and not device.checks.filter(check_type='tcp', port=443).exists():
        MonitoringCheck.objects.create(
            device=device,
            check_type='tcp',
            name='HTTPS Port',
            target=str(device.ip_address),
            port=443,
            interval_seconds=300,
        )
