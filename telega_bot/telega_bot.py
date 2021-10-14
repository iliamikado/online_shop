import telebot
import requests
import json


bot = telebot.TeleBot('2066788132:AAFGlJfhFWvImkODR0xz962kilfoC2do4-E')


@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, 'Добро пожаловать в онлайн-магазин. Напиши /help, чтобы узнать список команд')


@bot.message_handler(commands=['help'])
def help_message(message):
    bot.send_message(message.chat.id, '''/items - узнать доступные товары
/help - узнать список команд
/cat - получить котика
Чтобы забронировать товар напиши "забронировать *название_товара*"''')


@bot.message_handler(commands=['items'])
def help_message(message):
    with open('../data/parameters.json', 'r', encoding='utf-8') as file:
        param = json.load(file)
    stats = requests.get('http://' + param['server_address'] + ':' + str(param['server_port']) + '/api/stats').json()['data']
    bot.send_message(message.chat.id, get_items_description(stats))


def get_items_description(stats):
    s = 'У нас имеется:\n'
    for item in stats:
        s += item + ' (кол-во: ' + str(stats[item]) + ')\n'
    return s


@bot.message_handler(commands=['cat'])
def start_message(message):
    bot.send_message(message.chat.id, '''
───▐▀▄──────▄▀▌───▄▄▄▄▄▄▄
───▌▒▒▀▄▄▄▄▀▒▒▐▄▀▀▒██▒██▒▀▀▄
──▐▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▀▄
──▌▒▒▒▒▒▒▒▒▒▒▒▒▒▄▒▒▒▒▒▒▒▒▒▒▒▒▒▀▄
▀█▒▒█▌▒▒█▒▒▐█▒▒▀▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▌
▀▌▒▒▒▒▒▀▒▀▒▒▒▒▒▀▀▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▐ ▄▄
▐▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▄█▒█
▐▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒█▀
──▐▄▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▄▌
────▀▄▄▀▀▀▀▄▄▀▀▀▀▀▀▄▄▀▀▀▀▀▀▄▄▀
''')


@bot.message_handler(content_types=['text'])
def send_text(message):
    if message.text[:14] == 'забронировать ':
        with open('../data/parameters.json', 'r', encoding='utf-8') as file:
            param = json.load(file)
        bot.send_message(message.chat.id, 'начинаю бронь товара: ' + message.text[14:])
        request = requests.post('http://' + param['server_address'] + ':'
                                + str(param['server_port']) + '/api/reserve',
                                data={'username': 'Ilia', 'item': message.text[14:]})
        bot.send_message(message.chat.id, request.text)
    else:
        bot.send_message(message.chat.id, 'Я тебя не понял. Напиши /help, чтобы узнать меня получнше')


bot.polling(none_stop=True)
