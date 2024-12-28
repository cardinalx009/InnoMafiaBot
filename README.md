# 🎭 Mafia Bot

Telegram uchun Mafia o'yini statistikasini yurituvchi bot.

## 🚀 Imkoniyatlar

- O'yinchilar statistikasini yuritish
- Top o'yinchilar ro'yxatini ko'rish
- Shaxsiy statistikani ko'rish
- O'yin natijalarini saqlash
- Anti-spam tizimi

## 🛠 O'rnatish

1. Repositoriyani clone qiling:
```bash
git clone https://github.com/yourusername/mafia-bot.git
cd mafia-bot
```

2. Virtual muhit yarating va faollashtiring:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac uchun
# yoki
.\venv\Scripts\activate  # Windows uchun
```

3. Kerakli kutubxonalarni o'rnating:
```bash
pip install -r requirements.txt
```

4. `.env.example` faylidan `.env` fayl yarating va sozlamalarni kiriting:
```bash
cp .env.example .env
```

5. `.env` faylini tahrirlang va quyidagi ma'lumotlarni kiriting:
- Telegram bot tokeni (@BotFather dan olinadi)
- Firebase ma'lumotlar bazasi sozlamalari

## 🚀 Ishga tushirish

Botni ishga tushirish uchun:
```bash
python main.py
```

## 📝 Buyruqlar

- `/start` - Botni ishga tushirish
- `/info` - Bot haqida ma'lumot
- `/show` - Shaxsiy statistikani ko'rish
- `/top` - Top o'yinchilar ro'yxati

## 👥 Guruh sozlamalari

1. Botni guruhga qo'shing
2. Botga admin huquqlarini bering
3. Guruhda `/start` buyrug'ini yuboring

## 📄 Litsenziya

[MIT](LICENSE.md) © 2024
