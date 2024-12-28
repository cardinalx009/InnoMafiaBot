#!/bin/bash

# Screen sessiyasi mavjud bo'lsa o'chirish
screen -X -S mafia_bot quit

# Yangi screen sessiyasi yaratish
screen -dmS mafia_bot bash -c 'cd /home/user/Desktop/mafia && ./venv/bin/python main.py'

echo "Bot orqa fonda ishga tushirildi!"
echo "Bot loglarini ko'rish uchun: screen -r mafia_bot"
echo "Botni to'xtatish uchun: screen -X -S mafia_bot quit"
