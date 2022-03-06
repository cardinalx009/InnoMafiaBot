# Main code of mafia bot
# Catching messages to him and send some answers

# Global task
# TODO implement returning table for mafia
# TODO implement some answers for pm messages

# The nearest tasks
# TODO share to mafia group this bot
# TODO add image for bot

import dotenv
from os import getenv
from aiogram import Bot, Dispatcher, types, executor
from users_info import *

dotenv.load_dotenv(dotenv.find_dotenv())
bot = Bot(getenv("TOKEN"))
dp = Dispatcher(bot)


def get_markup() -> types.InlineKeyboardMarkup:
    keyboard = types.InlineKeyboardMarkup(resize_keyboard=True)
    keyboard.add(types.InlineKeyboardButton("Info", callback_data="info"))
    keyboard.add(types.InlineKeyboardButton("My statistics", callback_data="stats"))
    keyboard.add(types.InlineKeyboardButton("Top 3 people", callback_data="top"))
    keyboard.add(types.InlineKeyboardButton("Group url", url="https://t.me/innopolismafiaclub"))
    return keyboard


def generate_top(top: int) -> str:
    answer = "Top mafia people:\n"
    for i, (alias, info) in enumerate(
            sorted(parse_data(import_string()).items(), key=lambda p: p[1]['points'], reverse=True)[:top], start=1):
        answer += f"{i}: {alias} have {info['points']} points\n"
    return answer


@dp.message_handler(lambda message: message.text == "/stat", content_types=['text'])
async def send_statistic(message: types.Message):
    """Top 3 statistics"""
    top: int = 3
    await message.answer(generate_top(top), reply_markup=(get_markup() if message.from_user.id == message.chat.id else None))


@dp.message_handler(content_types=['text'])
async def get_text_messages(message: types.Message):
    """start message, introduction to functions of bot"""

    await message.reply(
        "Hello! I am Innopolis Mafia Bot.\n"
        "I can send you info about your games in this season or about your all-time stats.\n"
        "For more information write /info_bot.",
        reply_markup=get_markup()
    )


@dp.callback_query_handler(lambda c: c.data == "info")
async def inline_info(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(
        callback_query.from_user.id,
        "I am Innopolis Mafia Bot, I help host the games and collect data about players.\n"
        "Using me, you can get information about: game wins/loses, win rate, attendance and much more.\n"
        "For that you have to write /show or /personal_info.",
        reply_markup=get_markup()
    )


@dp.callback_query_handler(lambda c: c.data == "top")
async def inline_top(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, text=generate_top(3), reply_markup=get_markup())


@dp.callback_query_handler(lambda c: c.data == "stats")
async def inline_personal_info(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    alias = '@' + callback_query.from_user.username
    answer = ""

    try:
        player = parse_data(import_string())[alias]
        answer = "Your statistics:\nName: " + player["name"] + "\nID: " + player["id"] + "\nPoints: " + player["points"]
    except KeyError:
        answer = "Sorry, you are not in Rating System now\nReport about it to @Neph0 or @n1ce_timothy or play your first game."
    except:
        print("Connecting problem: " + alias + "is trying to check his grades.")
        answer = "Sorry, something went wrong, Report about it to @Neph0 or @n1ce_timothy."

    await bot.send_message(callback_query.from_user.id, text=answer, reply_markup=get_markup())


def start() -> None:
    """start the program (and bot)"""
    executor.start_polling(dp, skip_updates=True)


if __name__ == "__main__":
    start()
