# Bilmad NOC Sprint 2.2 Patch - Asset Engine UI

Bu patch Sprint 2.1 üzerine uygulanır.

## Gelen özellikler

- Assets ana ekranı: `/assets/`
- Asset detay ekranı: `/assets/<id>/`
- Customer360 detay ekranı: `/companies/<id>/`
- Integrations merkezi: `/integrations/`
- Sol menü güncellendi
- Status badge stilleri eklendi
- Mevcut `Device`, `Company`, `Location`, `Alert`, `Metric`, `Integration` modelleri korunur
- Migration gerektirmez

## Uygulama

ZIP içeriğini proje ana klasörüne çıkarıp üzerine yazdırın.

Sonra:

```bash
python manage.py runserver 0.0.0.0:8010
```

Kontrol URL'leri:

- http://127.0.0.1:8010/
- http://127.0.0.1:8010/assets/
- http://127.0.0.1:8010/companies/
- http://127.0.0.1:8010/integrations/

## Commit mesajı

```bash
git add .
git commit -m "Sprint 2.2: add asset engine and customer360 screens"
```
