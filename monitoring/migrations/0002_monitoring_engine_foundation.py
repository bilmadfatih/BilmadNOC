# Generated for Bilmad NOC Sprint 2.3 - Monitoring Engine Foundation
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ('monitoring', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='MonitoringCheck',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('check_type', models.CharField(choices=[('ping', 'Ping'), ('http', 'HTTP'), ('tcp', 'TCP Port')], default='ping', max_length=20, verbose_name='Check Tipi')),
                ('name', models.CharField(blank=True, max_length=120, verbose_name='Check Adı')),
                ('target', models.CharField(blank=True, max_length=255, verbose_name='Hedef')),
                ('port', models.PositiveIntegerField(blank=True, null=True, verbose_name='Port')),
                ('path', models.CharField(blank=True, default='/', max_length=255, verbose_name='Path')),
                ('interval_seconds', models.PositiveIntegerField(default=60, verbose_name='Periyot')),
                ('timeout_seconds', models.PositiveIntegerField(default=3, verbose_name='Timeout')),
                ('status', models.CharField(choices=[('enabled', 'Aktif'), ('disabled', 'Pasif')], default='enabled', max_length=20, verbose_name='Durum')),
                ('last_run_at', models.DateTimeField(blank=True, null=True, verbose_name='Son Çalışma')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Oluşturma')),
                ('device', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='checks', to='monitoring.device', verbose_name='Cihaz')),
            ],
            options={
                'verbose_name': 'Monitoring Check',
                'verbose_name_plural': 'Monitoring Checks',
                'ordering': ['device__company__name', 'device__name', 'check_type'],
            },
        ),
        migrations.CreateModel(
            name='CheckResult',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('success', models.BooleanField(default=False, verbose_name='Başarılı')),
                ('status', models.CharField(default='unknown', max_length=20, verbose_name='Sonuç')),
                ('response_time_ms', models.PositiveIntegerField(blank=True, null=True, verbose_name='Yanıt Süresi ms')),
                ('message', models.TextField(blank=True, verbose_name='Mesaj')),
                ('raw_data', models.JSONField(blank=True, default=dict, verbose_name='Ham Veri')),
                ('checked_at', models.DateTimeField(auto_now_add=True, verbose_name='Kontrol Zamanı')),
                ('monitoring_check', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='results', to='monitoring.monitoringcheck', verbose_name='Monitoring Check')),
                ('device', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='check_results', to='monitoring.device')),
            ],
            options={
                'verbose_name': 'Check Result',
                'verbose_name_plural': 'Check Results',
                'ordering': ['-checked_at'],
            },
        ),
        migrations.AddIndex(
            model_name='checkresult',
            index=models.Index(fields=['device', '-checked_at'], name='monitoring__device__e385b9_idx'),
        ),
        migrations.AddIndex(
            model_name='checkresult',
            index=models.Index(fields=['monitoring_check', '-checked_at'], name='monitoring__check_i_35aa88_idx'),
        ),
        migrations.AddIndex(
            model_name='checkresult',
            index=models.Index(fields=['success', '-checked_at'], name='monitoring__success_8a2988_idx'),
        ),
    ]
