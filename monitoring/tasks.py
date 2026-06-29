from monitoring.services.checks import run_all_enabled_checks, run_check, run_device_checks

try:
    from celery import shared_task
except Exception:  # Celery paket yoksa runserver kırılmasın.
    shared_task = None


if shared_task:
    @shared_task
    def run_all_checks_task():
        return len(run_all_enabled_checks())

    @shared_task
    def run_device_checks_task(device_id):
        from monitoring.models import Device
        device = Device.objects.get(pk=device_id)
        return len(run_device_checks(device))

    @shared_task
    def run_check_task(check_id):
        from monitoring.models import MonitoringCheck
        check = MonitoringCheck.objects.get(pk=check_id)
        result = run_check(check)
        return result.id
else:
    def run_all_checks_task():
        return len(run_all_enabled_checks())

    def run_device_checks_task(device_id):
        from monitoring.models import Device
        device = Device.objects.get(pk=device_id)
        return len(run_device_checks(device))

    def run_check_task(check_id):
        from monitoring.models import MonitoringCheck
        check = MonitoringCheck.objects.get(pk=check_id)
        result = run_check(check)
        return result.id
