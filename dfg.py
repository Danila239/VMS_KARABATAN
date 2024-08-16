from telebot import *
import random
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, timedelta
import pytz
# Вставьте сюда свой токен Telegram API
TOKEN = "7054824514:AAH6f-3UUfs6mFvo5ilBN9VN3aVgDhgjhd4"
bot = telebot.TeleBot(TOKEN)

CHAT_ID = "-4286479911"
local_tz = pytz.timezone('Asia/Karachi')


def send_scheduled_message():
    # Отправка сообщения в группу
    bot.send_message(CHAT_ID, "Это запланированное сообщение!")


def schedule_messages():
    scheduler = BackgroundScheduler()

    # Установка времени на 8:00 по GMT+5
    local_time = local_tz.localize(datetime.strptime('08:00:00', '%H:%M:%S')).time()
    utc_time = local_tz.normalize(
        pytz.utc.localize(datetime.combine(datetime.today(), local_time)).astimezone(pytz.utc)).time()

    # Запланировать выполнение задачи каждый день в 8:00 по GMT+5
    scheduler.add_job(send_scheduled_message, 'cron', hour=utc_time.hour, minute=utc_time.minute, timezone='UTC')

    # Запуск планировщика
    scheduler.start()


# Запуск планировщика сообщений
schedule_messages()



# Список из 12 значений
values = ['Линия AA', 'Линия AB', 'Линия AC', 'Линия AD', 'Линия AE', 'Линия AF',
          'Линия AG', 'Линия AH', 'Линия BB', 'Линия BC', 'Линия BD', 'Линия BE',
          'Линия BF', 'Линия BG', 'Линия BH']

# Настройка команд для всплывающего меню
commands = [
    telebot.types.BotCommand("start", "Приветствие"),
    telebot.types.BotCommand("get_values", "Получить случайные значения"),
]

# Установка команд для бота
bot.set_my_commands(commands)

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("👋 Поздороваться")
    markup.add(btn1)
    bot.send_message(message.chat.id, "Привет! Я VMS!", reply_markup=markup)

# Обработчик команды /get_values
@bot.message_handler(commands=['get_values'])
def send_random_values(message):
    random_values = random.sample(values, 4)  # Выбираем 4 случайных значения
    bot.reply_to(message, '\n'.join(random_values))

# Обработчик текстовых сообщений
@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    # Проверка на упоминание бота в сообщении
    if bot.get_me().username in message.text:
        if '👋 Поздороваться' in message.text:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)  # Создание новых кнопок
            btn1 = types.KeyboardButton('!')
            btn2 = types.KeyboardButton('!!')
            btn3 = types.KeyboardButton('!!!')
            markup.add(btn1, btn2, btn3)
            bot.reply_to(message, 'Нажми на любую кнопку', reply_markup=markup)  # Ответ бота

        elif any(keyword in message.text for keyword in ['!', '!!', '!!!']):
            random_values = random.sample(values, 4)
            bot.reply_to(message, '\n'.join(random_values))
    else:
        bot.reply_to(message, "Сообщение не распознано. Попробуйте другую команду.")


@bot.message_handler(func=lambda message: message.chat.id == CHAT_ID)
def handle_message(message):
    # Ответ на сообщение
    bot.reply_to(message, "Ваше сообщение было получено!")

# Запуск бота
bot.polling()
