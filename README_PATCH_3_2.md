# Bilmad NOC - Sprint 3.2 Discovery Engine Patch

Bu patch son yüklenen gerçek `BilmadNOC.zip` baseline'ı için hazırlanmıştır.

## İçerik

- `discovery` Django app eklendi.
- Keşif Merkezi ekranı eklendi: `/discovery/`
- IP aralığı TCP port tarama altyapısı eklendi.
- Bulunan hostlar için cihaz tipi önerisi eklendi.
- Keşif sonucu seçilen hostları `monitoring.Device` listesine aktarma eklendi.
- Mevcut `core.models` dosyasında `Company`, `Location`, `Workspace` uyumluluğu geri getirildi.
- Sol menüye `Keşif` bağlantısı eklendi.

## Uygulama

ZIP'i proje ana dizinine açıp üzerine yazdır.

```bash
python manage.py migrate
python manage.py runserver 0.0.0.0:8010
```

## Test

Tarayıcıdan aç:

```text
http://127.0.0.1:8010/discovery/
```

Örnek tarama:

```text
192.168.7.0/24
```

## Not

Bu ilk Discovery sürümü güvenli başlangıç sürümüdür. SNMP, ping sweep, celery async scan ve monitoring profile önerisi sonraki sprintlerde derinleştirilecektir.
