# Bilmad NOC v0.1.0 - Sprint 0.1 Core

## Eklenenler
- Çok müşterili çekirdek yapı
- Firma, lokasyon ve workspace modelleri
- Cihaz, metrik ve alarm modelleri
- Entegrasyon merkezi temel modeli
- Dark theme dashboard
- TV/NOC Wall ekranı
- Django admin kayıtları

## Çalıştırma
```cmd
cd C:\BilmadNOC
venv\Scripts\activate
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver 8010
```

Açılış:
- Dashboard: http://127.0.0.1:8010/
- NOC Wall: http://127.0.0.1:8010/noc-wall/
- Admin: http://127.0.0.1:8010/admin/
