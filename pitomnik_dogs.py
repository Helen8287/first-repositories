# Питомник / Разработка чат-бота с ИИ
# Идея: создание чат-бота для питомника собак.

# ✅ Функционал:
# - Общение с клиентами (продажа щенков и сопутствующих товаров)
# - Обработка входящих запросов...

# Идея: создание чат-бота для питомника собак.

# ✅ Функционал:
# - Общение с клиентами (продажа щенков и сопутствующих товаров)
# - Обработка входящих запросов
# - Запись на встречи в календарь
# - Уведомления



import time
import datetime
import logging
import telebot
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Установите токен вашего бота
TOKEN = 'YOUR_BOT_TOKEN'  # Убедитесь, что заменили токен на реальный
CHAT_ID = 'YOUR_CHAT_ID'  # ID чата, куда будет отправляться сообщение

# Настройка логирования
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Создаем экземпляр бота
bot = telebot.TeleBot(TOKEN)

# Установите соединение с Google Sheets
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name('path/to/your/credentials.json', scope)
client = gspread.authorize(creds)

# Откройте таблицу по имени
sheet = client.open("Имя вашей таблицы").sheet1

# Обработчик команды /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Добро пожаловать! Я бот питомника для собак. Чем могу помочь?")

# Обработчик команды /help
@bot.message_handler(commands=['help'])
def send_help(message):
    bot.reply_to(message, "Я помогу вам в решении ваших вопросов. Используйте команду /start, чтобы начать.")

# Обработчик команды /meetings
@bot.message_handler(commands=['meetings'])
def send_meetings(message):
    bot.reply_to(message, "Я могу записать вас на консультацию. Выберите, пожалуйста, удобную для вас дату и время.")

# Обработчик команды /puppies
@bot.message_handler(commands=['puppies'])
def send_puppies(message):
    bot.reply_to(message, "Я помогу вам с выбором щенка. Введите, пожалуйста, название породы.")

# Обработка текстовых сообщений (запрос породы)
@bot.message_handler(func=lambda message: True)
def handle_breed(message):
    breed = message.text.strip().capitalize()
    # Здесь вы можете добавить логику для обработки выбранной породы
    bot.reply_to(message, f"Вы выбрали породу: {breed}. Сейчас найду информацию о {breed}.")
    # Можно вызвать функцию для получения информации о щенках
    show_puppy_data(sheet, breed)

# Получение информации о щенках
def get_puppy_info(sheet, breed=None, sold=False):
    puppy_data = sheet.get_all_records()  # Получаем все записи
    result = []

    for record in puppy_data:
        if sold:
           if breed is None or record['Порода'] == breed:
                result.append({
                    'Порода': record['Порода'],
                    'Продано мальчиков': record['Продано мальчиков'],
                    'Продано девочек': record['Продано девочек']
                })
        else:
            if breed is None or record['Порода'] == breed:
                result.append({
                    'Порода': record['Порода'],
                    'Мальчики': record['Мальчики'],
                    'Девочки': record['Девочки'],
                    'Цена мальчика': record['Цена мальчика'],
                    'Цена девочки': record['Цена девочки']
                })
    return result

# Отображение данных о щенках
def show_puppy_data(sheet, breed=None, sold=False):
    puppy_info = get_puppy_info(sheet, breed, sold)

    if sold:
        response = "Проданные щенки по породам:\n"
        for record in puppy_info:
            response += f"{record['Порода']} - продано мальчиков {record['Продано мальчиков']} шт, " \
                        f"продано девочек {record['Продано девочек']} шт\n"
    else:
        response = "Наличие щенков по породам:\n"
        for record in puppy_info:
            response += f"{record['Порода']} - мальчики {record['Мальчики']} шт, девочки {record['Девочки']} шт\n" \
                        f"Цена: Мальчик - {record['Цена мальчика']} руб., Девочка - {record['Цена девочки']}руб.\n"

# Отправляем информацию пользователю
    bot.send_message(CHAT_ID, response)

# Продажа щенков
def handle_puppy_sale(sheet):
    puppy_breed = input("Введите породу щенка: ")
    male_price = input("Введите цену для мальчика: ")
    female_price = input("Введите цену для девочки: ")

    # Информация о продаже щенков
    print(f"Цена щенка породы {puppy_breed}:\nМальчик: {male_price}\nДевочка: {female_price}")

    # Записать информацию о продаже в Google Таблицы
    sheet.append_row(["Продажа щенка", puppy_breed, "Мальчик", male_price])
    sheet.append_row(["Продажа щенка", puppy_breed, "Девочка", female_price])
    print(f"Данные о продаже щенка породы {puppy_breed} добавлены в таблицу.")

# Продажа сопутствующих товаров
def sell_dog_products():
    print("Перенаправляем вас на сайт с товарами для собак: https://example.com/dog-products")
    product = input("Введите название товара: ").strip().lower()

  # Словарь с товарами и их ценами
    products = {
        'корм': {'price': 500, 'available': True},
        'игрушка': {'price': 300, 'available': True},
        'поводок': {'price': 150, 'available': False},
        # добавьте другие товары
    }

    if product in products:
        item = products[product]
        if item['available']:
            print(f"Товар '{product}' доступен. Цена: {item['price']} руб.")
            # Здесь можно добавить логику для оформления заказа
        else:
            print(f"Товар '{product}' временно недоступен.")
    else:
        print(f"Товар '{product}' не найден.")

if __name__ == "__main__":
    choice = input("Выберите действие (1 - Задать вопрос, 2 - Продажа щенков, 3 - Продажа товаров): ").strip()
    if choice == '1':
        question = input("Введите ваш вопрос: ")
        # Здесь можно добавить логику для обработки вопроса
        print(f"Вопрос клиента: {question} был получен и записан в таблицу.")
        # Записать вопрос в Google Таблицы
        sheet.append_row(["Вопрос", question])
    elif choice == '2':
        show_puppy_data(sheet, sold=False)  # Показать доступные щенки
        handle_puppy_sale(sheet)  # Обработка продажи щенков
    elif choice == '3':
        sell_dog_products()  # Обработка продажи сопутствующих товаров

bot.polling(none_stop=True)
