#!/bin/bash

# Loyiha papkasiga o'tish
cd /root/kirim_chiqim

# Virtual environment faollashtirish
source venv/bin/activate

# Paketlarni o'rnatish
pip install -r requirements.txt

# Migratsiyalarni qo'llash
python manage.py migrate --noinput

# Static fayllarni yig'ish
python manage.py collectstatic --noinput

# Gunicorn bilan ishga tushirish (port 8021)
gunicorn config.wsgi:application \
    --bind 0.0.0.0:8021 \
    --workers 3 \
    --timeout 120 \
    --access-logfile logs/access.log \
    --error-logfile logs/error.log \
    --daemon

echo "Server 8021-portda ishga tushdi!"
