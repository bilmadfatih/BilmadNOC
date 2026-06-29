def resolve_device_status(device, current_result=None):
    if current_result is not None:
        if current_result.success:
            return 'online'
        return 'critical' if device.is_critical else 'offline'

    latest = device.check_results.order_by('-checked_at').first()
    if latest is None:
        return device.status or 'unknown'
    if latest.success:
        return 'online'
    return 'critical' if device.is_critical else 'offline'
