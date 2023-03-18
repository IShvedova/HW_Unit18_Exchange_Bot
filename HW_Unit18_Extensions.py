import requests
import json
from HW_Unit18_Config import keys

class  APIException(Exception):
    pass

class Exchange:
    @staticmethod
    def get_price(quote: str, base: str, amount: str):
        if quote == base:
            raise APIException(f'\nНельзя конвертировать идентичные валюты "{base}"'
                               f'\nПопробуйте изменить одну из валют')

        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise APIException(f'\nДанной валюты нет в моей базе конвертации "{quote}" \n'
                               f'\nДля просмотра доступных к конвертации валют введите /values')

        try:
            base_ticker = keys[base]
        except KeyError:
            raise APIException(f'\nДанной валюты нет в моей базе конвертации "{base}" \n'
                               f'\nДля просмотра доступных к конвертации валют введите /values')

        try:
            amount = float(amount)

            if int(amount) > 0:
                amount = int(amount)
            else:
                raise APIException(f'\nОшибка ввода! {amount}\n'
                                   f'\nВведите положительное значение: ')

        except ValueError:
            raise APIException(f'\nОшибка ввода количества: {amount}\n'
                               f'\nДля просмотра доступных функций введите \n/help')

        r = requests.get(
            f'https://min-api.cryptocompare.com/data/price?fsym={quote_ticker}&tsyms={base_ticker}')
        total_base = json.loads(r.content)[keys[base]]
        return float(total_base * amount)

class DeclensionByCases():
    def __init__(self, word, num):
        self.word = word
        self.num = num

    def incline(self):
        if self.word != 'евро':
            if (2 <= self.num % 10 <= 4 and self.num % 100 not in [12, 13, 14]) or not self.num.is_integer():
                return 'рубля' if self.word == 'рубль' else self.word + 'a'
            if (self.num % 10 == 0 or 5 <= self.num % 10 <= 9 or 11 <= self.num % 100 <= 14) and self.num.is_integer():
                return 'рублей' if self.word == 'рубль' else self.word + 'ов'
        return self.word