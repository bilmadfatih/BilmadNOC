# Bilmad NOC - Sprint 3.0.1 Dil Hotfix

Bu patch, Sprint 3.0 sonrasında dil seçicinin daha görünür hale getirilmesi ve ana menü metinlerinin Türkçeleştirilmesi için hazırlanmıştır.

## Değişiklikler

- Sağ üst dil seçici `TR` yerine `🌐 Türkçe` olarak görünür hale getirildi.
- Dil seçenekleri `Türkçe / English` olarak düzenlendi.
- Sol menü Türkçeleştirildi:
  - Dashboard -> Ana Panel
  - Mission Control -> Operasyon Merkezi
  - Assets -> Varlıklar
  - Customers -> Müşteriler
  - Integrations -> Entegrasyonlar
  - Administration -> Yönetim
- Dil seçici için CSS görünürlük iyileştirmesi eklendi.

## Uygulama

ZIP içeriğini proje ana klasörüne çıkarıp üzerine yazdırın.

```bash
python manage.py runserver 0.0.0.0:8010
```

## Test

- Sağ üstte `🌐 Türkçe` görünmeli.
- Sol menü Türkçe görünmeli.
- `/cmdb/`, `/assets/`, `/companies/` sayfaları açılmalı.
