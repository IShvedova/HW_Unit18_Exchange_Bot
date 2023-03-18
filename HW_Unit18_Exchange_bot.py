import telebot
from HW_Unit18_Config import keys, TOKEN
from HW_Unit18_Extensions import APIException, Exchange, DeclensionByCases

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    text = f'Привет, {message.from_user.first_name}! \n\nЯ - конвертер валют' \
           f'\nЧтобы конвертировать валюту введите мне команду <имя валюты> <в какую валюту перевести> ' \
           f'<количество переводимой валюты>' \
           f'\nНапример,: рубль доллар 100\n' \
           f'\nЧтобы я показал доступные к конвертации валюты - введите \n/values;' \
           f'\nЧтобы просмотреть доступные функции введите \n/help.'
    bot.send_message(message.chat.id, text)

# Обрабатываем команду help:
@bot.message_handler(commands=['help'])
def help(message: telebot.types.Message):
    text = 'Чтобы перевести валюту, напишите команду следующим образом:' \
           '\n<имя валюты> <в какую валюту перевести> <количество переводимой валюты> через пробелы.' \
           '\nНапример: рубль евро 1\n' \
           '\nЧтобы увидеть валюты, которые я смогу конвертировать, введите команду\n/values'
    bot.reply_to(message, text)

@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text, key,))
    bot.reply_to(message, text)

@bot.message_handler(content_types=['text', ])
def get_price(message: telebot.types.Message):
    try:
        values = message.text.lower().split(' ')

        if len(values) != 3:
            raise APIException('\nВведено не 3 параметра!\n'
                                      '\nФормат ввода:\n<имя валюты> ' \
                                      '<в какую валюту перевести> <количество переводимой валюты> через пробелы')

        quote, base, amount = values
        total_base = Exchange.get_price(quote, base, amount)
    except APIException as e:
        bot.reply_to(message, f'Ошибка ввода! Проверьте введенные данные!\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Упс! Что-то пошло не так!\n\n{e}\n')
    else:
        inclined_quote = DeclensionByCases(quote, float(amount))
        inclined_base = DeclensionByCases(base, float(total_base))
        quote = inclined_quote.incline()
        base = inclined_base.incline()
        text = f'{amount} {quote} = {round(total_base, 5)} {base}'
        bot.send_message(message.chat.id, text)

bot.polling()