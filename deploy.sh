#!/bin/bash
# =============================================
# Serverga joylashtirish skripti
# Server: root@178.18.252.161  Port: 8021
# =============================================

SERVER="root@178.18.252.161"
REMOTE_DIR="/root/kirim_chiqim"

echo "==> Loyiha serverga ko'chirilmoqda..."
rsync -avz --exclude='venv/' \
           --exclude='__pycache__/' \
           --exclude='*.pyc' \
           --exclude='.git/' \
           --exclude='staticfiles/' \
           --exclude='logs/' \
           . $SERVER:$REMOTE_DIR

echo "==> Serverda sozlamalar qo'llanilmoqda..."
ssh $SERVER << 'EOF'
cd /root/kirim_chiqim

# Virtual environment yaratish (agar yo'q bo'lsa)
if [ ! -d "venv" ]; then
    python3 -m venv venv
fi

source venv/bin/activate

# Paketlarni o'rnatish
pip install -r requirements.txt -q

# Logs papkasi
mkdir -p logs

# Static fayllarni yig'ish
python manage.py collectstatic --noinput

# Migratsiyalarni qo'llash (mavjud ma'lumotlar saqlanib qoladi)
python manage.py migrate --noinput

# Systemd service o'rnatish
cp kirim_chiqim.service /etc/systemd/system/
systemctl daemon-reload
systemctl enable kirim_chiqim
systemctl restart kirim_chiqim

echo ""
echo "✓ Server holati:"
systemctl status kirim_chiqim --no-pager
echo ""
echo "✓ http://178.18.252.161:8021 manzilida ishlaydi!"
EOF
