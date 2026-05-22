#!/bin/bash
# Ma'lumotlar bazasini serverga yuklash
# Bu skript faqat bir marta ishlatiladi (birinchi o'rnatishda)

SERVER="root@178.18.252.161"

echo "==> db.sqlite3 serverga ko'chirilmoqda..."
scp db.sqlite3 $SERVER:/root/kirim_chiqim/db.sqlite3
echo "==> Ma'lumotlar bazasi muvaffaqiyatli ko'chirildi!"
