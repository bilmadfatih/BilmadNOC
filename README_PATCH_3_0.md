# Bilmad NOC - Sprint 3.0 CMDB + i18n Patch

## Amaç
Bu patch, Bilmad NOC'u CMDB tabanlı Operations Platform mimarisine taşımak için ilk veri modelini ve Türkçe/İngilizce dil altyapısını ekler.

## Eklenenler
- Yeni `cmdb` app'i
- Business Service modeli
- Application modeli
- Asset Relationship modeli
- Service Dependency modeli
- Backup Job modeli
- Admin yönetimi
- Basit CMDB overview ekranı: `/cmdb/`
- Django i18n altyapısı
- Varsayılan dil: Türkçe
- Dil seçenekleri: Türkçe / English
- Sağ üst dil seçici
- Menüye CMDB bağlantısı

## Migration
Var.

Çalıştır:

```bash
python manage.py migrate
```

## Test
```bash
python manage.py check
python manage.py migrate
python manage.py runserver 0.0.0.0:8010
```

Kontrol adresleri:

```text
http://127.0.0.1:8010/
http://127.0.0.1:8010/cmdb/
http://127.0.0.1:8010/admin/
```

## Not
Bu patch mevcut monitoring/asset akışını değiştirmez. CMDB modelleri mevcut `Company` ve `Device` modellerine bağlanır. Böylece çalışan ekranlar bozulmadan CMDB katmanı eklenir.
