# Generated for Bilmad NOC v0.2
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    initial = True
    dependencies = [('core', '0001_initial')]
    operations = [
        migrations.CreateModel(
            name='Device',
            fields=[('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')), ('name', models.CharField(max_length=150, verbose_name='Cihaz Adı')), ('device_type', models.CharField(choices=[('server', 'Sunucu'), ('vmware', 'VMware ESXi'), ('switch', 'Switch'), ('access_point', 'Access Point'), ('firewall', 'Firewall'), ('router', 'Router'), ('backup', 'Backup Sistemi'), ('sensway', 'Ortam Sensörü'), ('cctv_nvr', 'NVR/DVR'), ('cctv_camera', 'Kamera'), ('alarm_panel', 'Alarm Paneli'), ('m365', 'Microsoft 365'), ('security', 'Güvenlik Sistemi'), ('other', 'Diğer')], max_length=40, verbose_name='Cihaz Tipi')), ('vendor', models.CharField(blank=True, max_length=80, verbose_name='Marka')), ('model', models.CharField(blank=True, max_length=100, verbose_name='Model')), ('ip_address', models.GenericIPAddressField(blank=True, null=True, verbose_name='IP Adresi')), ('hostname', models.CharField(blank=True, max_length=150, verbose_name='Hostname')), ('is_critical', models.BooleanField(default=False, verbose_name='Kritik Cihaz')), ('status', models.CharField(choices=[('unknown', 'Bilinmiyor'), ('online', 'Online'), ('offline', 'Offline'), ('warning', 'Uyarı'), ('critical', 'Kritik')], default='unknown', max_length=20, verbose_name='Durum')), ('last_checked_at', models.DateTimeField(blank=True, null=True, verbose_name='Son Kontrol')), ('last_error', models.TextField(blank=True, verbose_name='Son Hata')), ('created_at', models.DateTimeField(auto_now_add=True)), ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='devices', to='core.company', verbose_name='Firma')), ('location', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='devices', to='core.location', verbose_name='Lokasyon'))],
            options={'verbose_name': 'Cihaz', 'verbose_name_plural': 'Cihazlar', 'ordering': ['company__name', 'name']},
        ),
        migrations.CreateModel(
            name='Metric',
            fields=[('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')), ('name', models.CharField(max_length=100)), ('value', models.FloatField(blank=True, null=True)), ('unit', models.CharField(blank=True, max_length=30)), ('collected_at', models.DateTimeField(auto_now_add=True)), ('device', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='metrics', to='monitoring.device'))],
            options={'verbose_name': 'Metrik', 'verbose_name_plural': 'Metrikler', 'ordering': ['-collected_at']},
        ),
        migrations.CreateModel(
            name='Alert',
            fields=[('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')), ('title', models.CharField(max_length=200, verbose_name='Başlık')), ('message', models.TextField(blank=True, verbose_name='Açıklama')), ('severity', models.CharField(choices=[('info', 'Bilgi'), ('warning', 'Uyarı'), ('critical', 'Kritik')], default='warning', max_length=20, verbose_name='Seviye')), ('is_resolved', models.BooleanField(default=False, verbose_name='Çözüldü')), ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Oluşturma')), ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='alerts', to='core.company')), ('device', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='alerts', to='monitoring.device'))],
            options={'verbose_name': 'Alarm', 'verbose_name_plural': 'Alarmlar', 'ordering': ['-created_at']},
        ),
    ]
