import telebot
from telebot import types
import datetime
import requests

bot = telebot.TeleBot('5590253922:AAEQR4eFmrbRx2B6rM_mlO7o9MZeTXemGuk')
open_weather_token = 'e57520f66424144a24f75a4c3ccefcf0'
birja = requests.get("https://www.cbr-xml-daily.ru/daily_json.js").json()
dollar = birja['Valute']['USD']['Previous']
euro = birja['Valute']['EUR']['Previous']
#wv - переменная валют и погоды, где погода - 1, валюты - 2
wv = 0

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.InlineKeyboardMarkup(row_width=2)
    item = types.InlineKeyboardButton('Погода', callback_data='weather')
    item1 = types.InlineKeyboardButton('Валюты', callback_data='bir')
    markup.add(item, item1)
    global wv
    wv = 0
    bot.send_message(message.chat.id, 'Выбери то, что ты хотел бы узнать у меня', reply_markup=markup)


@bot.message_handler(commands=['name'])
def name(message):
    mess = f'Привет <b>{message.from_user.first_name} {message.from_user.last_name}</b>'
    bot.send_message(message.chat.id, mess, parse_mode='html')

@bot.message_handler()
def get_weather(message):

    code_to_smile = {
        "Clear": "Ясно \U00002600",
        "Clouds": "Облачно \U00002601",
        "Rain": "Дождь \U00002614",
        "Drizzle": "Дождь \U00002614",
        "Thunderstorm": "Гроза \U000026A1",
        "Snow": "Снег \U0001F328",
        "Mist": "Туман \U0001F328",
    }
    try:
        if (wv == 1):

            r = requests.get(
                f"http://api.openweathermap.org/data/2.5/weather?q={message.text}&appid={open_weather_token}"
            )
            data = r.json()

            city = data["name"]
            cur_weather = data["main"]["temp"]

            weather_description = data["weather"][0]["main"]
            if weather_description in code_to_smile:
                wd = code_to_smile[weather_description]
            else:
                wd = "Посмотри в окно!"
            humidity = data["main"]["humidity"]
            pressure = data["main"]["pressure"]
            wind = data["wind"]["speed"]
            sunrice_timestamp = datetime.datetime.fromtimestamp(data["sys"]["sunrise"])
            sunset_timestamp = datetime.datetime.fromtimestamp(data["sys"]["sunset"])
            lenght_of_the_day = datetime.datetime.fromtimestamp(data["sys"]["sunset"]) - datetime.datetime.fromtimestamp(
                data["sys"]["sunrise"])
            markup = types.InlineKeyboardMarkup(row_width=1)
            item = types.InlineKeyboardButton('Выйти в меню', callback_data='Exit')
            markup.add(item)
            #Температура: {cur_weather}С° {wd}\n
            bot.send_message(message.chat.id, f"***{datetime.datetime.now().strftime('%Y-%m-%d-%H-%M')}***\n"
                                            f"Погода в городе: {city}\nПогода: {wd}\n"
                                            f"Влажность: {humidity}%\nДавление: {pressure} мм.рт.ст\nВетер: {wind} м/с\n"
                                            f"Восход солнца: {sunrice_timestamp}\nЗакат солнца: {sunset_timestamp}\nПродолжительность дня: {lenght_of_the_day}\n"
                                            f"Хорошего дня!", reply_markup=markup)
        else:
            bot.send_message(message.chat.id, "Выберите, что вы хотите сделать!", parse_mode='html')
    except:
        bot.send_message(message.chat.id, "Проверьте название города!", reply_markup=markup)


@bot.message_handler(commands=['name'])
def valfortimer(message):
    markup = types.InlineKeyboardMarkup(row_width=1)
    item = types.InlineKeyboardButton('Выйти в меню', callback_data='Exit')
    markup.add(item)
    bot.send_message(message.chat.id, "USD = " + str(dollar) + " рублей"
                "\nEUR = " + str(euro) + " рублей", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    if call.message:
        if call.data == 'weather':
            bot.send_message(call.message.chat.id, "Выберите или напишите город, который вас интересует!")
            global wv
            wv = 1
        if call.data == 'bir':
            markup1 = types.InlineKeyboardMarkup(row_width=1)
            item = types.InlineKeyboardButton('Выйти в меню', callback_data='Exit')
            markup1.add(item)
            bot.send_message(call.message.chat.id, "USD = " + str(dollar) + " рублей"
                             "\nEUR = " + str(euro) + " рублей", reply_markup=markup1)
        if call.data == 'Exit':
            markup2 = types.InlineKeyboardMarkup(row_width=2)
            item = types.InlineKeyboardButton('Погода', callback_data='weather')
            item1 = types.InlineKeyboardButton('Валюты', callback_data='bir')
            markup2.add(item, item1)
            wv = 0
            bot.send_message(call.message.chat.id, 'Привет, выбери то, что ты хотел бы узнать у меня', reply_markup=markup2)



bot.polling(none_stop=True)
