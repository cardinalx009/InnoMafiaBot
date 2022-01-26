import telebot

bot = telebot.TeleBot("5058417039:AAE8bbyEkehPSCLCDOcOC-z8aB75t5KEMQc")


@bot.message_handler(content_types=['text'], commands=["start"])
def get_text_messages(message):
    """start message, introduction to functions of bot"""
    bot.reply_to(message, "Hello! I am Innopolis Mafia Bot.\n"
                          "I can send you personal info about your games in this season or all time")


@bot.message_handler(commands=["info_bot", "bot_info"])
def get_info_about_bot(message):
    """global information about bot"""
    bot.reply_to(message, "I am Innopolis Mafia Bot, I help host in game and collect some data about players.\n"
                          "You can get information about: game wins/loses, win rate, attendance and other.\n"
                          "For that you have to write your personal id or telegram alias.")


@bot.message_handler(commands=["personal_info"])
def send_personal_info(message):
    """write personal info to user"""
    bot.reply_to(message, "")


bot.infinity_polling()
