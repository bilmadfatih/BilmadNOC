# Bilmad NOC v0.3.0

Çok müşterili, modüler NOC / CCTV / Alarm / IT operasyon platformu başlangıç sürümü.

## Çalıştırma

```cmd
cd C:\BilmadNOC
venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py seed_demo
python manage.py runserver 8010
```

## Ekranlar

- Dashboard: http://127.0.0.1:8010/
- NOC Wall: http://127.0.0.1:8010/noc-wall/
- CCTV / Alarm Wall: http://127.0.0.1:8010/security-wall/
- Admin: http://127.0.0.1:8010/admin/

## v0.3.0 Özeti

Bu sürümde TV/monitor ekranı için NOC Wall ve CCTV/Alarm Wall görsel olarak iyileştirildi.
