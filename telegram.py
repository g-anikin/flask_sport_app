import telebot
from DatabaseInterface import DatabaseInterface

bot = telebot.TeleBot('1160243033:AAFEk6_aban4IQ69A_jEqlqGPskkaXTzmwk')
keyboard = telebot.types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
button_phone = telebot.types.KeyboardButton(text="Отправить номер телефона", request_contact=True)
button_geo = telebot.types.KeyboardButton(text="Отправить местоположение", request_location=True)
keyboard.add(button_phone, button_geo)


@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, 'Привет, выбор за тобой!', reply_markup=keyboard)


@bot.message_handler(commands=['show_db'])
def start_message(message):
    connect_to_db = DatabaseInterface('exercise.db')
    connect_to_db.select_from_db()
    s = ''
    for i in connect_to_db.select_from_db():
        s = s + '\n'
        for j in i:
            s = s + str(j) + ' '
    bot.send_message(message.chat.id, s)


bot.polling()
