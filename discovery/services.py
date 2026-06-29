import ipaddress
import socket
from concurrent.futures import ThreadPoolExecutor, as_completed

from .models import DiscoveryHost

COMMON_PORTS = [22, 80, 443, 554, 3389, 5900, 8080, 8443, 8728, 8291, 9100]
PORT_TIMEOUT = 0.28
MAX_HOSTS = 512
MAX_WORKERS = 64


def _scan_port(ip, port):
    try:
        with socket.create_connection((str(ip), port), timeout=PORT_TIMEOUT):
            return port
    except OSError:
        return None


def _resolve_hostname(ip):
    try:
        return socket.gethostbyaddr(str(ip))[0]
    except OSError:
        return ''


def _guess_type(open_ports):
    ports = set(open_ports)
    if 902 in ports or (443 in ports and 22 in ports and 80 not in ports):
        return 'vmware', 85, 'VMware / Hypervisor'
    if 8291 in ports or 8728 in ports:
        return 'router', 90, 'MikroTik / Router'
    if 9100 in ports:
        return 'other', 80, 'Network Printer'
    if 554 in ports:
        return 'cctv_camera', 80, 'Camera / NVR'
    if 3389 in ports:
        return 'server', 75, 'Windows Server'
    if 22 in ports and (80 in ports or 443 in ports):
        return 'switch', 65, 'Network Device'
    if 22 in ports:
        return 'server', 60, 'Linux / Network Device'
    if 80 in ports or 443 in ports or 8080 in ports or 8443 in ports:
        return 'other', 55, 'Web Device'
    return 'other', 40, 'Unknown Device'


def run_discovery(discovery_run):
    discovery_run.mark_running()
    try:
        network = ipaddress.ip_network(discovery_run.cidr, strict=False)
        hosts = list(network.hosts())[:MAX_HOSTS]
        found = {}

        with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
            futures = {}
            for ip in hosts:
                for port in COMMON_PORTS:
                    futures[executor.submit(_scan_port, ip, port)] = str(ip)

            for future in as_completed(futures):
                port = future.result()
                if port:
                    found.setdefault(futures[future], []).append(port)

        for ip, ports in found.items():
            ports = sorted(set(ports))
            dtype, confidence, label = _guess_type(ports)
            hostname = _resolve_hostname(ip)
            suggested_name = hostname or f'{label}-{ip}'
            DiscoveryHost.objects.update_or_create(
                discovery_run=discovery_run,
                ip_address=ip,
                defaults={
                    'hostname': hostname,
                    'suggested_name': suggested_name[:180],
                    'suggested_type': dtype,
                    'open_ports': ports,
                    'confidence': confidence,
                },
            )
        discovery_run.mark_completed()
    except Exception as exc:
        discovery_run.mark_failed(exc)
        raise


def import_hosts_to_devices(discovery_run, host_ids=None):
    queryset = discovery_run.hosts.all()
    if host_ids:
        queryset = queryset.filter(id__in=host_ids)

    imported = 0
    for host in queryset:
        if host.imported_device_id:
            continue

        device, created = discovery_run.company.devices.get_or_create(
            ip_address=host.ip_address,
            defaults={
                'location': discovery_run.location,
                'name': host.suggested_name or host.hostname or str(host.ip_address),
                'device_type': host.suggested_type,
                'hostname': host.hostname,
                'status': 'unknown',
            },
        )
        if not created:
            device.location = device.location or discovery_run.location
            device.hostname = device.hostname or host.hostname
            device.device_type = device.device_type or host.suggested_type
            device.save(update_fields=['location', 'hostname', 'device_type'])

        host.imported_device = device
        host.save(update_fields=['imported_device'])
        imported += 1
    return imported
