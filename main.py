# Main code of mafia bot
# Catching messages to him and send some answers

# Global task
# TODO implement returning table for mafia
# TODO implement some answers for pm messages

# The nearest tasks
# TODO share to mafia group this bot
# TODO add image for bot

from aiogram import Bot, Dispatcher, types, executor
from users_info import *

bot = Dispatcher(Bot("5058417039:AAE8bbyEkehPSCLCDOcOC-z8aB75t5KEMQc"))


@bot.message_handler(content_types=['text'], commands=["start"])
async def get_text_messages(message: types.Message):
    """start message, introduction to functions of bot"""
    await message.reply("Hello! I am Innopolis Mafia Bot.\n"
                        "I can send you info about your games in this season or about your all-time stats.\n"
                        "For more information write /info_bot.")


@bot.message_handler(commands=["info_bot", "bot_info"])
async def get_info_about_bot(message: types.Message):
    """global information about bot"""
    await message.reply("I am Innopolis Mafia Bot, I help host the games and collect data about players.\n"
                        "Using me, you can get information about: game wins/loses, win rate, attendance and much more.\n"
                        "For that you have to write /show or /personal_info.")


@bot.message_handler(commands=["personal_info", "show"])
async def send_personal_info(message: types.Message):
    """write personal info to user"""
    alias = '@' + message.chat.username
    answer: str

    try:
        player = parse_data(import_string())[alias]
        answer = "Name: " + player["name"] + "\nID: " + player["id"] + "\nPoints: " + player["points"]
    except KeyError:
        answer = "Sorry, you are not in Rating System now\nReport about it to @Neph0 or @n1ce_timothy or play your first game."
    except:
        print("Connecting problem: " + alias + "is trying to check his grades.")
        answer = "Sorry, something went wrong, Report about it to @Neph0 or @n1ce_timothy."
    await message.reply(answer)


def start() -> None:
    """start the program (and bot)"""
    executor.start_polling(bot, skip_updates=True)


if __name__ == "__main__":
    start()
