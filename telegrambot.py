import main
import telebot
from telebot import types

bot = telebot.TeleBot("token")

main.train_model()


# Обработка команды /start
@bot.message_handler(commands=['start'])
def start(message):
    user_id=message.from_user.id
    keyboard=types.ReplyKeyboardMarkup(is_persistent=True,resize_keyboard=True)
    keyboard.row("Узнать цену")
    bot.send_message(user_id, "Здравствуйте, я могу предположить, какая цена будет у квартиры в Москве, зная некоторые ее параметры. Давайте попробуем?",reply_markup=keyboard)


# Обработка команды Узнать цену
@bot.message_handler(func=lambda message: message.text == "Узнать цену")
def predict_price(message):
    user_id = message.from_user.id
    params = {"Минут до метро": 0, "Количество комнат": 0, "Площадь": 0, "Площадь спален": 0, "Площадь кухни": 0,
              "Номер этажа": 0, "Количетво этажей": 0,
              "Восточный административный округ": 0, "Западный административный округ": 0,
              "Новомосковский административный округ": 0, "Северный административный округ": 0,
              "Северо-Восточный административный округ": 0, "Северо-Западный административный округ": 0,
              "Центральный административный округ": 0, "Юго-Восточный административный округ": 0,
              "Юго-Западный административный округ": 0, "Южный административный округ": 0,
              "Без ремонта": 0, "Дизайнерский": 0, "Европейский": 0, "Косметический": 0}
    bot.send_message(user_id, "Для начала введите количество минут от квартиры до метро: ")
    bot.register_next_step_handler(message, get_minutes_to_metro, params)

def get_minutes_to_metro(message,params):
    user_id = message.from_user.id
    try:
        min_to_metro=int(message.text)
        params["Минут до метро"]=min_to_metro
        bot.send_message(user_id, "Введите количество комнат в квартире: ")
        bot.register_next_step_handler(message, get_cnt_rooms, params)
    except:
        bot.send_message(user_id, "Введённое значение должно быть числом! Введите количество минут от квартиры до метро: ")
        bot.register_next_step_handler(message, get_minutes_to_metro, params)


def get_cnt_rooms(message,params):
    user_id = message.from_user.id
    try:
        cnt_rooms=int(message.text)
        params["Количество комнат"]=cnt_rooms
        bot.send_message(user_id, "Введите площадь квартиры: ")
        bot.register_next_step_handler(message, get_all_square, params)
    except:
        bot.send_message(user_id, "Введённое значение должно быть числом! Введите количество комнат в квартире: ")
        bot.register_next_step_handler(message, get_cnt_rooms, params)


def get_all_square(message,params):
    user_id = message.from_user.id
    try:
        all_square = int(message.text)
        params["Площадь"] = all_square
        bot.send_message(user_id, "Введите площадь спален: ")
        bot.register_next_step_handler(message, get_beadroom_square, params)
    except:
        bot.send_message(user_id, "Введённое значение должно быть числом! Введите площадь квартиры: ")
        bot.register_next_step_handler(message, get_all_square, params)


def get_beadroom_square(message,params):
    user_id = message.from_user.id
    try:
        beadroom_square = int(message.text)
        params["Площадь спален"] = beadroom_square
        bot.send_message(user_id, "Введите площадь кухни: ")
        bot.register_next_step_handler(message, get_kitchen_square, params)
    except:
        bot.send_message(user_id, "Введённое значение должно быть числом! Введите площадь спален: ")
        bot.register_next_step_handler(message, get_beadroom_square, params)


def get_kitchen_square(message,params):
    user_id = message.from_user.id
    try:
        kitchen_square = int(message.text)
        params["Площадь кухни"] = kitchen_square
        bot.send_message(user_id, "Введите номер этажа: ")
        bot.register_next_step_handler(message, get_stage, params)
    except:
        bot.send_message(user_id, "Введённое значение должно быть числом! Введите площадь кухни: ")
        bot.register_next_step_handler(message, get_kitchen_square, params)


def get_stage(message,params):
    user_id = message.from_user.id
    try:
        stage = int(message.text)
        params["Номер этажа"] = stage
        bot.send_message(user_id, "Введите количество этажей: ")
        bot.register_next_step_handler(message, get_all_stages, params)
    except:
        bot.send_message(user_id, "Введённое значение должно быть числом! Введите номер этажа: ")
        bot.register_next_step_handler(message, get_stage, params)


def get_all_stages(message,params):
    user_id = message.from_user.id
    try:
        all_stages = int(message.text)
        params["Количетво этажей"] = all_stages
        keyboard= types.ReplyKeyboardMarkup(is_persistent=True,resize_keyboard=True)
        keyboard.row("Восточный административный округ")
        keyboard.row("Западный административный округ")
        keyboard.row("Новомосковский административный округ")
        keyboard.row("Северный административный округ")
        keyboard.row("Северо-Восточный административный округ")
        keyboard.row("Северо-Западный административный округ")
        keyboard.row("Центральный административный округ")
        keyboard.row("Юго-Восточный административный округ")
        keyboard.row("Юго-Западный административный округ")
        keyboard.row("Южный административный округ")
        bot.send_message(user_id, "Выберите округ: ",reply_markup=keyboard)
        bot.register_next_step_handler(message, get_region, params)
    except:
        bot.send_message(user_id, "Введённое значение должно быть числом! Введите количество этажей: ")
        bot.register_next_step_handler(message, get_all_stages, params)


def get_region(message,params):
    user_id = message.from_user.id
    region=message.text
    if region in params:
        params[region]=1
        keyboard=types.ReplyKeyboardMarkup(is_persistent=True,resize_keyboard=True)
        keyboard.row("Без ремонта")
        keyboard.row("Дизайнерский")
        keyboard.row("Европейский")
        keyboard.row("Косметический")
        bot.send_message(user_id, "Выберите тип ремонта в квартире: ", reply_markup=keyboard)
        bot.register_next_step_handler(message, get_remont, params)
    else:
        keyboard = types.ReplyKeyboardMarkup(is_persistent=True,resize_keyboard=True)
        keyboard.row("Восточный административный округ")
        keyboard.row("Западный административный округ")
        keyboard.row("Новомосковский административный округ")
        keyboard.row("Северный административный округ")
        keyboard.row("Северо-Восточный административный округ")
        keyboard.row("Северо-Западный административный округ")
        keyboard.row("Центральный административный округ")
        keyboard.row("Юго-Восточный административный округ")
        keyboard.row("Юго-Западный административный округ")
        keyboard.row("Южный административный округ")
        bot.send_message(user_id, "Неизвестный регион! Выберите округ: ",reply_markup=keyboard)
        bot.register_next_step_handler(message, get_region, params)

def get_remont(message,params):
    user_id = message.from_user.id
    remont=message.text
    if remont in params:
        params[remont]=1
        price=main.get_price(params)
        formatted_number = "{:,.0f}".format(price).replace(',', '.')
        keyboard = types.ReplyKeyboardMarkup(is_persistent=True,resize_keyboard=True)
        keyboard.row("Узнать цену")
        bot.send_message(user_id, f"Я предполагаю, что цена за данную квартиру в Москве будет: {formatted_number} руб.", reply_markup=keyboard)
    else:
        keyboard = types.ReplyKeyboardMarkup(is_persistent=True,resize_keyboard=True)
        keyboard.row("Без ремонта")
        keyboard.row("Дизайнерский")
        keyboard.row("Европейский")
        keyboard.row("Косметический")
        bot.send_message(user_id, "Неизвестный тип! Выберите тип ремонта в квартире: ", reply_markup=keyboard)
        bot.register_next_step_handler(message, get_remont, params)

#Обработка неизвестной команды
@bot.message_handler(func=lambda message: True)
def handle_all_other_messages(message):
    bot.send_message(message.chat.id, 'Неизвестная команда')
    start(message)

# Запуск бота
bot.polling(none_stop=True)
