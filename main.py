"""
Mafia botining asosiy kodi
Xabarlarni qabul qilish va javob berish
"""
__author__ = "Zener085, cutefluffyfox"
__version__ = "2.0.1"
__license__ = "MIT"

from aiogram import Bot, Dispatcher, types, executor
from time import time
import json
import os
from dotenv import load_dotenv, find_dotenv

# Load token from .env file
load_dotenv(find_dotenv())
TOKEN = "7717119224:AAHXJx_ONAi3HY2MQLINFs-VVXp7Zknjj74"

bot = Bot(TOKEN)
dp = Dispatcher(bot)

# Local storage for players
PLAYERS_FILE = "players.json"
players_data = {}

def save_players():
    """Save players data to file"""
    with open(PLAYERS_FILE, 'w', encoding='utf-8') as f:
        json.dump(players_data, f, ensure_ascii=False, indent=2)

def load_players():
    """Load players data from file"""
    global players_data
    if os.path.exists(PLAYERS_FILE):
        with open(PLAYERS_FILE, 'r', encoding='utf-8') as f:
            players_data = json.load(f)

def get_markup() -> types.InlineKeyboardMarkup:
    """Bot asosiy funksiyalari uchun menyu tugmalari"""
    keyboard = types.InlineKeyboardMarkup(resize_keyboard=True)
    keyboard.add(types.InlineKeyboardButton("Ma'lumot", callback_data="info"))
    keyboard.add(types.InlineKeyboardButton("Mening statistikam", callback_data="personal_info"))
    keyboard.add(types.InlineKeyboardButton("Top o'yinchilar", callback_data="top"))
    keyboard.add(types.InlineKeyboardButton("Guruh linki", url="https://t.me/UzMafia"))
    return keyboard

@dp.message_handler(commands=['start'])
async def start_cmd(message: types.Message):
    """Start buyrug'ini qayta ishlash"""
    await message.reply(
        "Assalomu alaykum! Men Mafia o'yini botiman.\n"
        "Men sizga o'yin statistikangizni ko'rsata olaman.\n"
        "Ko'proq ma'lumot olish uchun /help buyrug'ini yuboring.",
        reply_markup=get_markup()
    )

@dp.message_handler(commands=['help'])
async def help_cmd(message: types.Message):
    """Help buyrug'ini qayta ishlash"""
    help_text = (
        "🎮 Mavjud buyruqlar:\n\n"
        "/start - Botni ishga tushirish\n"
        "/help - Yordam xabarini ko'rsatish\n"
        "/stats - Statistikani ko'rsatish\n"
        "/top - Top o'yinchilarni ko'rsatish\n\n"
        "❓ Savollar uchun: @admin"
    )
    await message.reply(help_text)

@dp.callback_query_handler(lambda c: c.data == "info")
async def process_info(callback_query: types.CallbackQuery):
    """Info tugmasini qayta ishlash"""
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(
        callback_query.from_user.id,
        "🎭 Mafia - bu jamoaviy o'yin.\n\n"
        "O'yin davomida har bir o'yinchi ma'lum bir rolni bajaradi.\n"
        "Mafiya a'zolari tinch aholini yo'q qilishga harakat qiladi,\n"
        "tinch aholi esa mafiya a'zolarini topishga harakat qiladi.\n\n"
        "Batafsil ma'lumot uchun: /help",
        reply_markup=get_markup()
    )

@dp.callback_query_handler(lambda c: c.data == "personal_info")
async def process_personal_info(callback_query: types.CallbackQuery):
    """Personal info tugmasini qayta ishlash"""
    user_id = str(callback_query.from_user.id)
    
    if user_id not in players_data:
        players_data[user_id] = {
            "games": 0,
            "wins": 0,
            "losses": 0,
            "name": callback_query.from_user.full_name
        }
        save_players()
    
    player = players_data[user_id]
    win_rate = (player["wins"] / player["games"] * 100) if player["games"] > 0 else 0
    
    stats = (
        f"📊 Statistika: {player['name']}\n\n"
        f"🎮 Jami o'yinlar: {player['games']}\n"
        f"🏆 G'alabalar: {player['wins']}\n"
        f"💀 Mag'lubiyatlar: {player['losses']}\n"
        f"📈 G'alaba foizi: {win_rate:.1f}%"
    )
    
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, stats, reply_markup=get_markup())

@dp.callback_query_handler(lambda c: c.data == "top")
async def process_top(callback_query: types.CallbackQuery):
    """Top players tugmasini qayta ishlash"""
    sorted_players = sorted(
        players_data.items(),
        key=lambda x: (x[1]["wins"], -x[1]["games"]),
        reverse=True
    )[:10]
    
    top_text = "🏆 Top o'yinchilar:\n\n"
    for i, (_, player) in enumerate(sorted_players, 1):
        win_rate = (player["wins"] / player["games"] * 100) if player["games"] > 0 else 0
        top_text += (
            f"{i}. {player['name']}\n"
            f"   ├ O'yinlar: {player['games']}\n"
            f"   ├ G'alabalar: {player['wins']}\n"
            f"   └ Foiz: {win_rate:.1f}%\n\n"
        )
    
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, top_text, reply_markup=get_markup())

def start():
    """Botni ishga tushirish"""
    load_players()
    executor.start_polling(dp, skip_updates=True)

if __name__ == "__main__":
    start()
