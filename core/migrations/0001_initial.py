# Generated for Bilmad NOC v0.2
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    initial = True
    dependencies = [migrations.swappable_dependency(settings.AUTH_USER_MODEL)]
    operations = [
        migrations.CreateModel(
            name='Company',
            fields=[('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')), ('name', models.CharField(max_length=200, verbose_name='Firma Adı')), ('short_name', models.CharField(blank=True, max_length=80, verbose_name='Kısa Ad')), ('health_score', models.PositiveIntegerField(default=100, verbose_name='Sağlık Skoru')), ('is_active', models.BooleanField(default=True, verbose_name='Aktif')), ('notes', models.TextField(blank=True, verbose_name='Notlar')), ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Oluşturma'))],
            options={'verbose_name': 'Firma', 'verbose_name_plural': 'Firmalar', 'ordering': ['name']},
        ),
        migrations.CreateModel(
            name='Location',
            fields=[('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')), ('name', models.CharField(max_length=150, verbose_name='Lokasyon')), ('address', models.TextField(blank=True, verbose_name='Adres')), ('is_active', models.BooleanField(default=True, verbose_name='Aktif')), ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='locations', to='core.company', verbose_name='Firma'))],
            options={'verbose_name': 'Lokasyon', 'verbose_name_plural': 'Lokasyonlar', 'ordering': ['company__name', 'name']},
        ),
        migrations.CreateModel(
            name='Workspace',
            fields=[('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')), ('name', models.CharField(max_length=150, verbose_name='Çalışma Alanı')), ('workspace_type', models.CharField(choices=[('noc', 'NOC Workspace'), ('it', 'IT Workspace'), ('network', 'Network Workspace'), ('cctv', 'CCTV Workspace'), ('alarm', 'Alarm Workspace'), ('executive', 'Yönetici Workspace'), ('partner', 'Partner Workspace')], max_length=30, verbose_name='Tip')), ('can_view_it', models.BooleanField(default=False)), ('can_view_network', models.BooleanField(default=False)), ('can_view_cctv', models.BooleanField(default=False)), ('can_view_alarm', models.BooleanField(default=False)), ('can_view_security', models.BooleanField(default=False)), ('companies', models.ManyToManyField(blank=True, related_name='workspaces', to='core.company', verbose_name='Firmalar')), ('users', models.ManyToManyField(blank=True, related_name='workspaces', to=settings.AUTH_USER_MODEL, verbose_name='Kullanıcılar'))],
            options={'verbose_name': 'Çalışma Alanı', 'verbose_name_plural': 'Çalışma Alanları'},
        ),
    ]
