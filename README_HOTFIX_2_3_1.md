# Bilmad NOC Sprint 2.3.1 Hotfix

Bu paket Sprint 2.3 sonrasında oluşan Django system check hatasını düzeltir.

## Düzeltilen hata

`monitoring.CheckResult.check` alan adı Django'nun dahili `Model.check()` metodu ile çakışıyordu.

Alan adı şu şekilde değiştirildi:

- Eski: `check`
- Yeni: `monitoring_check`

## Uygulama

Proje ana klasörüne açıp üzerine yazdırın.

Sonra çalıştırın:

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py runserver 0.0.0.0:8010
```

Eğer `0002_monitoring_engine_foundation` migration'ı henüz uygulanmadıysa doğrudan çalışacaktır.
