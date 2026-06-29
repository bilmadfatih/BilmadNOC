# Bilmad NOC Sprint 3.1 - CMDB Seed + Service Map

Bu patch CMDB ekranını boş bir model olmaktan çıkarıp ilk servis haritası seviyesine taşır.

## İçerik

- `seed_cmdb_demo` management command
- CMDB overview ekranında servis, uygulama, ilişki, dependency ve backup job panelleri
- Mevcut asset kayıtlarından örnek servis bağımlılığı üretimi
- Migration yok

## Kurulum

Projeye üzerine yazdırın.

```bash
python manage.py runserver 0.0.0.0:8010
```

CMDB demo verisi üretmek için:

```bash
python manage.py seed_cmdb_demo
```

Sonra kontrol:

```text
http://127.0.0.1:8010/cmdb/
```

## Commit Mesajı

```bash
git add .
git commit -m "Sprint 3.1: add CMDB demo seed and service map panels"
```
