# Bilmad NOC Sprint 2.1 Stabilizasyon Patch

Bu patch, önceki Sprint 2 paketinden sonra oluşan şu hatayı düzeltir:

```text
ImportError: cannot import name 'Company' from 'core.models'
```

## Ne değişti?

- `core.models` içine mevcut çalışan sistemin beklediği eski modeller geri eklendi:
  - `Company`
  - `Location`
  - `Workspace`
- Yeni Sprint 2 modelleri korunarak ileriye dönük bırakıldı:
  - `Tenant`
  - `Customer`
  - `Site`
  - `AuditLog`
- `core.admin` hem eski hem yeni modelleri gösterecek şekilde düzenlendi.
- `core/migrations/0002_sprint2_forward_core.py` eklendi.

## Uygulama

ZIP içeriğini proje ana klasörüne kopyala ve üzerine yaz.

Sonra çalıştır:

```bash
python manage.py migrate
python manage.py runserver 0.0.0.0:8010
```

Tarayıcı:

```text
http://127.0.0.1:8010
```

## Commit mesajı

```bash
git add core/models.py core/admin.py core/migrations/0002_sprint2_forward_core.py
git commit -m "Sprint 2.1: stabilize legacy core models and add forward core migration"
```
