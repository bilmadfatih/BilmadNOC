from django.core.management.base import BaseCommand

from monitoring.services.checks import run_all_enabled_checks


class Command(BaseCommand):
    help = 'Bilmad NOC monitoring checklerini manuel çalıştırır.'

    def handle(self, *args, **options):
        results = run_all_enabled_checks()
        ok = sum(1 for r in results if r.success)
        fail = len(results) - ok
        self.stdout.write(self.style.SUCCESS(f'Checks completed: {len(results)} total, {ok} ok, {fail} fail'))
