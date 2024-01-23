import telebot

bot = telebot.TeleBot('6532561146:AAGvEUL_A4rN3GKzwGr5Bu5dUpZrC9DQAhQ')


@bot.message_handler(commands=['start'])
def start(messge):
    mess = f'Privet <b>{messge.from_user.first_name} <u>{messge.from_user.last_name}</u></b>'
    bot.send_message(messge.chat.id, mess, parse_mode='html')


@bot.message_handler()
def get_user_text(message):
    bot.send_message(message.chat.id, message, parse_mode='html')


bot.polling(none_stop=True)
