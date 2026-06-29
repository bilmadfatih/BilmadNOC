# Bilmad NOC - Sprint 2 Core Engine

Bu paket mevcut Django projesine kopyalanacak Sprint 2 temel dosyalarını içerir.

## Gelen Modüller

- core: Tenant, Customer, Site, AuditLog, BaseModel
- assets: Asset Engine, Manufacturer, Location, AssetMetric
- plugins: MonitoringPlugin, PluginCheck, PluginResult
- mission_control: Dashboard view/template
- customer360: Müşteri 360 detay ekranı

## Kurulum

1. Bu ZIP içeriğini proje ana dizinine kopyalayın.
2. `settings.py` içine ekleyin:

```python
INSTALLED_APPS += [
    "core",
    "assets",
    "plugins",
    "mission_control",
    "customer360",
]
```

3. Ana `urls.py` içine ekleyin:

```python
from django.urls import include, path

urlpatterns += [
    path("", include("mission_control.urls")),
    path("customers/", include("customer360.urls")),
]
```

4. Migration çalıştırın:

```bash
python manage.py makemigrations
python manage.py migrate
```

5. Admin kullanıcısı yoksa oluşturun:

```bash
python manage.py createsuperuser
```

## Commit Planı

```bash
git checkout -b sprint-2-core-engine
git add .
git commit -m "Sprint 2: add core platform models"
git commit -m "Sprint 2: add asset engine foundation"
git commit -m "Sprint 2: add plugin framework foundation"
git commit -m "Sprint 2: add mission control and customer360 screens"
git push origin sprint-2-core-engine
```

## Sonraki Paket

Sprint 2.2 ile gerçek monitoring başlar:

- Redis
- Celery
- Ping check task
- TCP check task
- HTTP check task
- PluginResult otomatik kayıt
