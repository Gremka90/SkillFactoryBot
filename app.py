import telebot
from config import keys, TOKEN
from Extensions import ConvertionExeption, get_price

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def hellow(message: telebot.types.Message):
    text = 'Что бы начать работу введите команду боту в следующеи формате: \n<Имя валюты> \
<в какую валюту перевести> \
<количество переводимой валюты>\nУвидеть список доступных валют: /values'
    bot.reply_to(message, text)


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты'
    for key in keys.keys():
        text = '\n'.join((text, key, ))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text', ])
def convert(message: telebot.types.Message):
    try:
        values = message.text.split(' ')

        if len(values) != 3:
            raise ConvertionExeption('Слишком много параметров.')

        quote, base, amount = values
        total_base = get_price.convert(quote, base, amount)
    except ConvertionExeption as e:
        bot.reply_to(message, f'Ошибка пользователя\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду\n{e}')
    else:
        text = f'Цена {amount} {quote} в {base} = {total_base * float(amount)}'
        bot.send_message(message.chat.id, text)


bot.polling()