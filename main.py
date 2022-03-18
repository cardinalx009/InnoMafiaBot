# Main code of mafia bot
# Catching messages to him and send some answers

# Global task
# TODO implement some answers for pm messages

from aiogram import Bot, Dispatcher, types, executor
from time import time
from users_info import *

load_dotenv(find_dotenv())

bot = Bot(getenv("TOKEN"))
dp = Dispatcher(bot)
prev_player: Player = Player("", "-1", "Kasper", '0', '0')
prev_time: int = int(time())
spam_list: list[Player] = []


def get_markup() -> types.InlineKeyboardMarkup:
    """Menu buttons, included main functions for bot"""
    keyboard = types.InlineKeyboardMarkup(resize_keyboard=True)
    keyboard.add(types.InlineKeyboardButton("Info", callback_data="info"))
    keyboard.add(types.InlineKeyboardButton("My statistics", callback_data="personal_info"))
    keyboard.add(types.InlineKeyboardButton("Top 3 people", callback_data="top"))
    keyboard.add(types.InlineKeyboardButton("Group url", url="https://t.me/InnopolisMafia"))
    return keyboard


@dp.message_handler(content_types=['text'], commands=["start"])
async def get_text_messages(message: types.Message):
    """Start message, introduction to functions of bot"""

    await message.reply(
        "Hello! I am Innopolis Mafia Bot.\n"
        "I can send you info about your games in this season or about your all-time stats.\n"
        "For more information write /info_bot.",
        reply_markup=get_markup()
    )


@dp.callback_query_handler(lambda c: c.data in ["info", "info_bot", "bot_info"])
async def about(callback_query: types.CallbackQuery):
    """Send info about bot"""
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(
        callback_query.from_user.id,
        "I am Innopolis Mafia Bot, I help host the games and collect data about players.\n"
        "Using me, you can get information about: game wins/loses, win rate, attendance and much more.\n"
        "For that you have to write /show or /personal_info.",
        reply_markup=get_markup()
    )


@dp.callback_query_handler(lambda c: c.data in ["top", "top_rating", "rating", "stat"])
async def rating(callback_query: types.CallbackQuery):
    """Send top rating to group chat, using buttons"""
    global prev_player, prev_time, spam_list

    alias = '@' + callback_query.from_user.username
    try:
        player = parse_data(import_string())[alias]
    except KeyError:
        await bot.answer_callback_query(callback_query.id)
        await bot.send_message(callback_query.message.chat.id, text=top_rating(), reply_markup=get_markup())
        return

    # antispam system
    if prev_player.id == player.id and prev_time <= int(time()) + 30 and player not in spam_list:
        spam_list.append(player)
        print(player.alias)

    if player not in spam_list:
        await bot.answer_callback_query(callback_query.id)
        await bot.send_message(callback_query.message.chat.id, text=top_rating(), reply_markup=get_markup())
    prev_time = int(time())
    prev_player = player


@dp.message_handler(commands=["top", "top_rating", "rating", "stat"])
async def rating(message: types.Message):
    """Send top rating to group chat using commands"""
    global prev_player, prev_time, spam_list
    alias = '@' + message.from_user.username
    try:
        player = parse_data(import_string())[alias]
    except KeyError:
        await bot.send_message(message.chat.id, text=top_rating(), reply_markup=get_markup())
        return
    # antispam system

    if prev_player.id == player.id and prev_time <= int(time()) + 30 and player not in spam_list:
        spam_list.append(player)
        print(player.alias)

    if player not in spam_list:
        await bot.answer_callback_query(message.chat.id)
        await bot.send_message(message.chat.id, text=top_rating(), reply_markup=get_markup())
    prev_time = int(time())
    prev_player = player


@dp.callback_query_handler(lambda c: c.data in ["personal_info", "personal_statistics", "personal", "show"])
async def personal_info(callback_query: types.CallbackQuery):
    """Send personal info, only to private chat"""
    await bot.answer_callback_query(callback_query.id)
    alias = '@' + callback_query.from_user.username

    try:
        player = parse_data(import_string())[alias]
        answer = "Your statistics: " + player.to_string()
    except KeyError:
        answer = "Sorry, you are not in Rating System now\nReport about it to @Neph0 or @n1ce_timothy or play your " \
                 "first game."
    except:
        print("Connecting problem: " + alias + " is trying to check his grades.")
        answer = "Sorry, something went wrong, Report about it to @Neph0 or @n1ce_timothy."

    await bot.send_message(callback_query.from_user.id, text=answer, reply_markup=get_markup())


@dp.message_handler(commands="reactiveNeph0n1ce_timothy")
async def reactivate_players(message: types.Message):
    global spam_list, prev_player
    spam_list.clear()
    prev_player = Player()
    await message.reply(text="All players are active", reply_markup=get_markup())


def start() -> None:
    """start the program (and bot)"""
    executor.start_polling(dp, skip_updates=True)


if __name__ == "__main__":
    start()
