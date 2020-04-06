from datetime import datetime
import urllib.parse as urllib
from typing import Dict

import requests
from requests.auth import HTTPBasicAuth


def qr_parser(qr_text: str) -> Dict:
    """ Функция получения параметров чека из QRtext"""
    receipt_data = {}
    try:
        data = urllib.urlparse(qr_text)
        receipt_params = urllib.parse_qs(data.path, strict_parsing=True)
        for key, values in receipt_params.items():
            receipt_data[key] = values[0]
        #  Из QR кода должны приходить ровно 6ть параметров
        assert len(receipt_data) == 6
    except AssertionError:
        print('Количество параметров в QR коде не верное')
        return {}
    except ValueError:
        print('Информация в QR коде не в формате параметр=значение')
        return {}
    except AttributeError:
        print('QR код передан не в строковом формате')
        return {}
    return receipt_data


def registration_fns(email: str, name: str, phone: str) -> str:
    """
    Функция для регистрации пользователя в ФНС
    Ответы сервера: 204 - Успешно, 409 -User exist, 500 - Некорректный номер, 400 - некорректный email
    """
    registration_url = 'https://proverkacheka.nalog.ru:9999/v1/mobile/users/signup'
    data = {
        'email': email,
        'name': name,
        'phone': phone
    }
    try:
        registration_request = requests.post(registration_url, json=data)
        status_code = registration_request.status_code
        text = registration_request.text
        if status_code != 204:
            return text
        else:
            return 'Регистрация успешна'
    except requests.RequestException:
        return 'Сетевая ошибка'
    except ValueError:
        return 'Пользователь уже создан или неправильный формат телефона / email'


def recovery_pass(phone: str) -> str:
    """"
    Функция востановления пароля ФНС
    Ответы сервера: 204 - Успешно, 404 - Not found
    """
    recovery_url = 'https://proverkacheka.nalog.ru:9999/v1/mobile/users/restore'
    data = {'phone': phone}
    try:
        recovery_request = requests.post(recovery_url, json=data)
        status_code = recovery_request.status_code
        text = recovery_request.text
        if status_code != 204:
            return text
        else:
            return 'Запрос восстановления пароля выполнен успешно. Ожидайте СМС'
    except requests.RequestException:
        return 'Сетевая ошибка'
    except ValueError:
        return 'Незарегистрированная учетная запись'


# функцию вынес для записи в базу данных корректного формата дата\время
def format_date(raw_datetime: str) -> str:
    if len(raw_datetime) == 13:  # если в формате не учтены секунды добавляем 00 секунд
        raw_datetime = raw_datetime + '00'
    try:
        date = datetime.strptime(raw_datetime, '%Y%m%dT%H%M%S')
        return date.strftime('%Y-%m-%dT%H:%M')
    except ValueError:
        print('Не возможно распарсить строку date time')
        return False


def check_receipt(receipt_data: Dict) -> bool:  # TODO таймаут, счетчик
    """
    Функция проверки валидности чека
    Ответы сервера: 204 - Чек найден(, 406 - Не найден или сумма(дата) некоректны, 400 - Не указанна дата(сумма)
    500 - irkkt db timeout
    """

    # date_string = receipt_data['t']
    # if len(date_string) == 13:  # если в формате не учтены секунды добавляем 00 секунд
    #     date_string = date_string + '00'
    # try:
    #     date = datetime.strptime(date_string, '%Y%m%dT%H%M%S')
    #     format_date = date.strftime('%Y-%m-%dT%H:%M')
    # except ValueError:
    #     print('Не возможно распарсить строку date time')
    #     return False

    try:
        sum = int(float(receipt_data['s']) * 100)
        path = '/v1/ofds/*/inns/*/fss/' + receipt_data['fn'] + '/operations/' + receipt_data['n'] + '/tickets/' + \
               receipt_data['i']
        query = 'fiscalSign=' + receipt_data['fp'] + '&date=' + format_date(receipt_data['t']) + '&sum=' + str(sum)
        par = ('https', 'proverkacheka.nalog.ru:9999', path, '', query, '')
        url_check_receipt = urllib.urlunparse(par)
        print(url_check_receipt)
    except KeyError:
        print('Неизвестный ключ словаря')
        return False

    try:
        check_receipt = requests.get(url_check_receipt)
        status_code = check_receipt.status_code
        text = check_receipt.text
        if status_code != 204:
            print(status_code, text)
        else:
            return True
    except requests.RequestException:
        print('Сетевая ошибка')
        return False
    except ValueError:
        print('Неверный формат передаваемых данных')
        return False


def get_receipt(receipt_data: Dict, login: str, password: int) -> Dict:
    """
    Функция получения полных данных по кассовому чеку
    ВАЖНО! первый запрос по чеку приходит пустой необходимо сделать повторный запрос
    """
    headers = {
        'device-id': '',
        'device-os': '',
    }
    try:
        url_receipt = 'https://proverkacheka.nalog.ru:9999/v1/inns/*/kkts/*/fss/' + receipt_data['fn'] + \
                      '/tickets/' + receipt_data['i'] + '?fiscalSign=' + receipt_data['fp'] + \
                      '&sendToEmail=no'
    except KeyError:
        print('Неизвестный ключ словаря')
        return {}

    try:
        full_receipt = requests.get(url_receipt, auth=HTTPBasicAuth(login, password), headers=headers)
        full_receipt.raise_for_status()
        data = full_receipt.json()
        return data
    except requests.RequestException:
        print('Сетевая ошибка')
        return {}
    except ValueError:
        print(full_receipt.status_code, full_receipt.text)
        return {}


if __name__ == '__main__':
    a = format_date('20200325T0841')
    print(a)