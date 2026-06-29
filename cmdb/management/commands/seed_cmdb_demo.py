from django.core.management.base import BaseCommand
from django.utils import timezone

from core.models import Company
from monitoring.models import Device
from cmdb.models import (
    Application,
    AssetRelationship,
    BackupJob,
    BusinessService,
    Dependency,
    RelationshipType,
    ServiceCriticality,
)


class Command(BaseCommand):
    help = "Create a safe demo CMDB map from existing customers and assets."

    def handle(self, *args, **options):
        company = Company.objects.filter(is_active=True).order_by("name").first()
        if not company:
            self.stdout.write(self.style.WARNING("No active company found. Create a customer first."))
            return

        devices = list(Device.objects.filter(company=company).order_by("name"))
        if not devices:
            self.stdout.write(self.style.WARNING(f"No asset found for {company.name}. Create assets first."))
            return

        service, _ = BusinessService.objects.get_or_create(
            company=company,
            name="Operasyon Kritik Servisler",
            defaults={
                "owner": "NOC Ekibi",
                "criticality": ServiceCriticality.CRITICAL,
                "description": "CMDB demo servis haritası. Kritik varlıklar ve uygulamalar bu servis altında ilişkilendirilir.",
            },
        )
        service.devices.add(*devices[:6])

        primary = self._find_device(devices, ["server", "vmware", "firewall"]) or devices[0]
        app, _ = Application.objects.get_or_create(
            company=company,
            name="İş Uygulamaları",
            defaults={
                "service": service,
                "primary_device": primary,
                "criticality": ServiceCriticality.HIGH,
                "description": "CMDB etkilenme analizi için örnek uygulama kaydı.",
            },
        )
        if not app.service:
            app.service = service
        if not app.primary_device:
            app.primary_device = primary
        app.save()

        for device in devices[:6]:
            Dependency.objects.get_or_create(
                service=service,
                asset=device,
                defaults={
                    "description": f"{service.name} için gerekli varlık",
                    "is_required": device.is_critical or device == primary,
                    "impact_weight": 80 if device.is_critical or device == primary else 50,
                },
            )

        # Create a small relationship graph: network/core assets protect or host others.
        firewall = self._find_device(devices, ["firewall"])
        switch = self._find_device(devices, ["switch"])
        server = self._find_device(devices, ["server", "vmware"])
        backup = self._find_device(devices, ["backup"])

        relation_count = 0
        relation_count += self._rel(firewall, server, RelationshipType.PROTECTS, "Firewall protects server segment", 85)
        relation_count += self._rel(switch, server, RelationshipType.CONNECTED_TO, "Core network uplink", 75)
        relation_count += self._rel(server, app.primary_device, RelationshipType.HOSTS, "Application hosting dependency", 90)
        relation_count += self._rel(backup, server, RelationshipType.BACKED_UP_BY, "Backup protection", 80)

        backup_job, _ = BackupJob.objects.get_or_create(
            company=company,
            name="Kritik Sistem Yedekleme",
            defaults={
                "provider": "Narbulut / Veeam",
                "schedule": "Günlük 23:00",
                "last_status": "unknown",
                "last_run_at": timezone.now(),
                "notes": "CMDB demo yedekleme görevi.",
            },
        )
        backup_job.protected_assets.add(*devices[:4])

        self.stdout.write(self.style.SUCCESS(f"CMDB demo map created for {company.name}."))
        self.stdout.write(f"Service: {service.name}")
        self.stdout.write(f"Dependencies: {service.dependencies.count()}")
        self.stdout.write(f"Relationships created/verified: {relation_count}")
        self.stdout.write(f"Backup job: {backup_job.name}")

    def _find_device(self, devices, types):
        for device in devices:
            if device.device_type in types:
                return device
        return None

    def _rel(self, source, target, relation_type, label, weight):
        if not source or not target or source == target:
            return 0
        AssetRelationship.objects.get_or_create(
            source=source,
            target=target,
            relationship_type=relation_type,
            defaults={"label": label, "impact_weight": weight},
        )
        return 1
