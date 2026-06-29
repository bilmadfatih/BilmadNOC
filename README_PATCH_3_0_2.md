# Bilmad NOC Sprint 3.0.2 - Language Switch Hotfix

## Amaç
- Sağ üst dil seçicinin gerçekten TR/EN değiştirmesi.
- Base template metinlerini `{% trans %}` ile çeviri sistemine bağlamak.
- İngilizce `django.mo` çeviri dosyasını eklemek.
- `django.template.context_processors.i18n` context processor eklemek.

## Uygulama
ZIP içeriğini proje ana klasörüne açıp üzerine yazdırın.

## Çalıştırma
```bash
python manage.py runserver 0.0.0.0:8010
```

## Test
- Sağ üstten `🌐 English` seçin.
- Sol menüde `Ana Panel` -> `Dashboard`, `Varlıklar` -> `Assets` olmalı.
- Sonra tekrar `🌐 Türkçe` seçin.
