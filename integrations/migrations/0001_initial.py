# Generated for Bilmad NOC v0.2
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    initial = True
    dependencies = [('core', '0001_initial')]
    operations = [
        migrations.CreateModel(
            name='Integration',
            fields=[('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')), ('name', models.CharField(max_length=150, verbose_name='Entegrasyon Adı')), ('integration_type', models.CharField(choices=[('berqnet', 'Berqnet SASE'), ('vmware', 'VMware ESXi / vCenter'), ('narbulut', 'Narbulut Backup'), ('sensway', 'Sensway Ortam İzleme'), ('bitdefender', 'Bitdefender GravityZone'), ('m365', 'Microsoft 365'), ('cctv', 'CCTV / NVR'), ('alarm', 'Alarm Sistemi'), ('snmp', 'SNMP Network'), ('other', 'Diğer')], max_length=40, verbose_name='Tip')), ('status', models.CharField(choices=[('not_configured', 'Yapılandırılmadı'), ('connected', 'Bağlı'), ('error', 'Hata'), ('disabled', 'Pasif')], default='not_configured', max_length=30, verbose_name='Durum')), ('base_url', models.URLField(blank=True, verbose_name='API / Panel URL')), ('username', models.CharField(blank=True, max_length=150, verbose_name='Kullanıcı Adı')), ('notes', models.TextField(blank=True, verbose_name='Notlar')), ('last_sync_at', models.DateTimeField(blank=True, null=True, verbose_name='Son Senkronizasyon')), ('is_active', models.BooleanField(default=True, verbose_name='Aktif')), ('created_at', models.DateTimeField(auto_now_add=True)), ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='integrations', to='core.company', verbose_name='Firma'))],
            options={'verbose_name': 'Entegrasyon', 'verbose_name_plural': 'Entegrasyonlar', 'ordering': ['company__name', 'name']},
        ),
    ]
