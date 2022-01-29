from aiogram import Bot, Dispatcher, types, executor
from users_info import *

bot = Dispatcher(Bot("5058417039:AAE8bbyEkehPSCLCDOcOC-z8aB75t5KEMQc"))


@bot.message_handler(content_types=['text'], commands=["start"])
async def get_text_messages(message: types.Message):
    """start message, introduction to functions of bot"""
    await message.reply("Hello! I am Innopolis Mafia Bot.\n"
                          "I can send you personal info about your games in this season or all time")


@bot.message_handler(commands=["info_bot", "bot_info"])
async def get_info_about_bot(message: types.Message):
    """global information about bot"""
    await message.reply("I am Innopolis Mafia Bot, I help host in game and collect some data about players.\n"
                          "You can get information about: game wins/loses, win rate, attendance and other.\n"
                          "For that you have to write your personal id or telegram alias.")


@bot.message_handler(commands=["personal_info"])
async def send_personal_info(message: types.Message):
    """write personal info to user"""
    await message.reply()


if __name__ == "__main__":
    executor.start_polling(bot, skip_updates=True)
