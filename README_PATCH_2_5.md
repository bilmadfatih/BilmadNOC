# Bilmad NOC - Sprint 2.5 Monitoring Core + Health Engine

## Amaç
Bu patch, Sprint 2.4.1 üzerine uygulanacak şekilde hazırlanmıştır.

## Gelenler
- Monitoring Engine klasör yapısı
- Plugin registry altyapısı
- Ping / HTTP / TCP plugin sınıfları
- Health Score hesaplama servisi
- Asset listesindeki satırların tamamen tıklanabilir olması
- Asset listesine ikon + health puanı + son kontrol görünümü
- Asset Detail içinde health nedenleri ve plugin son sonuçları
- Dashboard kartlarının ilgili liste sayfalarına linklenmesi

## Migration
Yok.

## Uygulama
ZIP içeriğini proje ana klasörüne çıkarıp üzerine yazdırın.

```bash
python manage.py runserver 0.0.0.0:8010
```

## Test
- `/assets/` açılır.
- Bir asset satırının herhangi bir yerine tıklayınca detay sayfası açılır.
- Asset detayında `Şimdi Kontrol Et` çalışır.
- Health Score ve Monitoring Timeline görünür.

## Commit Mesajı
```bash
git add .
git commit -m "Sprint 2.5: add monitoring core and health engine"
```
