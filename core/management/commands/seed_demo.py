from django.core.management.base import BaseCommand
from core.models import Company, Location, Workspace
from monitoring.models import Device, Alert
from integrations.models import Integration


class Command(BaseCommand):
    help = 'Bilmad NOC demo verilerini oluşturur.'

    def handle(self, *args, **options):
        lima, _ = Company.objects.get_or_create(name='Lima Logistics', defaults={'short_name': 'Lima', 'health_score': 91})
        bilmad, _ = Company.objects.get_or_create(name='Bilmad İç Sistem', defaults={'short_name': 'Bilmad', 'health_score': 96})
        bursa, _ = Location.objects.get_or_create(company=lima, name='Bursa Merkez')
        atasehir, _ = Location.objects.get_or_create(company=lima, name='Ataşehir')
        noc, _ = Workspace.objects.get_or_create(name='Bilmad NOC Operasyon', workspace_type='noc', defaults={'can_view_it': True, 'can_view_network': True, 'can_view_cctv': True, 'can_view_alarm': True, 'can_view_security': True})
        cctv, _ = Workspace.objects.get_or_create(name='Partner CCTV & Alarm', workspace_type='cctv', defaults={'can_view_cctv': True, 'can_view_alarm': True})
        noc.companies.add(lima, bilmad)
        cctv.companies.add(lima)
        devices = [
            (lima, bursa, 'TR01 Berqnet SASE', 'firewall', 'Berqnet', 'online'),
            (lima, bursa, 'ESXi-01', 'vmware', 'VMware', 'warning'),
            (lima, bursa, 'Aruba Core Switch', 'switch', 'Aruba', 'online'),
            (lima, bursa, 'Narbulut Backup', 'backup', 'Narbulut', 'critical'),
            (lima, bursa, 'Sensway Server Room', 'sensway', 'Sensway', 'online'),
            (lima, atasehir, 'NVR-01', 'cctv_nvr', 'Hikvision', 'warning'),
            (lima, atasehir, 'Kamera-Depo-02', 'cctv_camera', 'Dahua', 'offline'),
            (lima, bursa, 'Ajax Panel Bursa', 'alarm_panel', 'Ajax', 'online'),
        ]
        created = 0
        for company, location, name, dtype, vendor, status in devices:
            obj, was_created = Device.objects.get_or_create(company=company, name=name, defaults={'location': location, 'device_type': dtype, 'vendor': vendor, 'status': status})
            created += int(was_created)
        integrations = [
            ('Berqnet SASE Lima', 'berqnet', 'connected'),
            ('VMware Lima', 'vmware', 'not_configured'),
            ('Narbulut Lima', 'narbulut', 'not_configured'),
            ('Bitdefender GravityZone', 'bitdefender', 'not_configured'),
            ('Microsoft 365 Tenant', 'm365', 'not_configured'),
            ('CCTV Partner', 'cctv', 'not_configured'),
        ]
        for name, itype, status in integrations:
            Integration.objects.get_or_create(company=lima, name=name, defaults={'integration_type': itype, 'status': status})
        nar = Device.objects.filter(name='Narbulut Backup').first()
        cam = Device.objects.filter(name='Kamera-Depo-02').first()
        esx = Device.objects.filter(name='ESXi-01').first()
        alerts = [
            (lima, nar, 'Narbulut son yedek başarısız', 'Son job hata verdi. API veya mail parser ile takip edilecek.', 'critical'),
            (lima, cam, 'Kamera-Depo-02 offline', 'Partner CCTV workspace üzerinde görüntülenmeli.', 'critical'),
            (lima, esx, 'ESXi datastore %88', 'Disk kapasitesi izlenmeli.', 'warning'),
        ]
        for company, device, title, message, severity in alerts:
            Alert.objects.get_or_create(company=company, device=device, title=title, defaults={'message': message, 'severity': severity})
        self.stdout.write(self.style.SUCCESS(f'Demo verileri hazır. Yeni cihaz: {created}'))
