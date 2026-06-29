# Bilmad NOC Sprint 2.3 Patch - Monitoring Engine Foundation

Bu patch Sprint 2.2.1 üzerine uygulanır.

## Gelen özellikler

- MonitoringCheck modeli
- CheckResult modeli
- Ping / HTTP / TCP servis altyapısı
- Asset detayında "Şimdi Kontrol Et" butonu
- Asset detayında check listesi ve sonuç timeline
- Dashboard üzerinde son monitoring sonuçları
- Manuel komut: `python manage.py run_checks`
- Celery hazır task iskeleti: `monitoring/tasks.py`

## Uygulama

ZIP içeriğini proje ana klasörüne çıkarıp üzerine yazdırın.

Sonra:

```bash
python manage.py migrate
python manage.py runserver 0.0.0.0:8010
```

## Kullanım

1. Tarayıcıdan `/assets/` sayfasına gir.
2. Bir asset adına tıkla.
3. Sağ üstteki **Şimdi Kontrol Et** butonuna bas.
4. Ping sonucu, asset durumu, metric ve alarm bilgisi ekrana düşer.

Toplu manuel kontrol:

```bash
python manage.py run_checks
```

## Commit mesajı

```bash
git add .
git commit -m "Sprint 2.3: add monitoring engine foundation"
```
