# Bilmad NOC Sprint 2.6 Patch

## Kapsam

Sprint 2.6, mevcut çalışan v0.5 hattını bozmadan Asset Detail ekranını derinleştirir.

Eklenen / iyileştirilenler:

- Asset listesinde durum ikonları ve health nedeni özeti
- Asset detail üst metrikleri: uptime/başarı, ortalama yanıt, son kontrol
- Plugin kartları: Ping / HTTP / TCP durum görünümü
- Monitoring timeline sparkline şeridi
- Performance preview kartları
- Dashboard son monitoring sonuçlarından asset detail ekranına hızlı geçiş
- Firma sağlık tablosunda satır tıklanabilirliği

## Migration

Yok.

## Uygulama

ZIP içeriğini proje ana klasörüne açıp üzerine yazdır.

```bash
python manage.py runserver 0.0.0.0:8010
```

## Test

- http://127.0.0.1:8010/assets/
- Bir asset satırına tıkla
- "Şimdi Kontrol Et" butonuna bas
- Timeline, plugin kartları ve health kartlarının güncellendiğini kontrol et
