from telebot import *
import random
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
import logging

# Вставьте сюда свой токен Telegram API
TOKEN = "7054824514:AAH6f-3UUfs6mFvo5ilBN9VN3aVgDhgjhd4"
bot = telebot.TeleBot(TOKEN)

CHAT_ID = "-4286479911"

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def send_periodic_message():
    try:
        bot.send_message(CHAT_ID, "Это ваше сообщение каждый день в 8 утра.")
        logger.info("Сообщение отправлено.")
    except Exception as e:
        logger.error(f"Ошибка при отправке сообщения: {e}")

# Настройка планировщика
scheduler = BackgroundScheduler()
scheduler.start()

# Добавление задачи в планировщик
scheduler.add_job(
    send_periodic_message,
    CronTrigger(hour=9, minute=33),  # Каждый день в 8:00
    id='daily_message_job',
    name='Отправка сообщения каждый день в 8 утра',
    replace_existing=True
)

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
    elif 'ы' in message.text:
        bot.reply_to(message, "ы")
    else:
        bot.reply_to(message, "Сообщение не распознано. Попробуйте другую команду.")

# Запуск бота
bot.polling()
