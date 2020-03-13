from datetime import datetime
import urllib.parse as urllib
import requests
from requests.auth import HTTPBasicAuth


def qr_parser(qr_text: str) -> dict:
    """ Функция получения параметров чека из QRtext"""
    receipt_data = {}
    try:
        data = urllib.urlparse(qr_text)
        receipt_params = urllib.parse_qs(data.path, strict_parsing=True)
        for key, values in receipt_params.items():
            receipt_data[key] = values[0]
        #  Из QR кода должны приходить ровно 6ть параметров
        assert len(receipt_data) == 6
    except (AssertionError, ValueError, AttributeError):
        print('Информация с QR кода некорректна')
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
            return 'Registration OK'
    except (requests.RequestException, ValueError):
        return 'Network error or registration failed'


def recovery_pass(phone: str) -> str:
    """"
    Функция востановления пароля ФНС
    Ответы сервера: 204 - Успешно, 404 - Not found
    """
    recovery_url = 'https://proverkacheka.nalog.ru:9999/v1/mobile/users/restore'
    data = {'phone': phone}
    try:
        recovery_request = requests.post(recovery_url , json=data)
        status_code = recovery_request.status_code
        text = recovery_request.text
        if status_code != 204:
            return text
        else:
            return 'Recovery password OK. Wait SMS'
    except (requests.RequestException, ValueError):
        return 'Network error or registration failed'


def check_receipt(receipt_data: dict) -> str:  # TODO проверить работоспособность на реальных данных
    """
    Функция проверки валидности чека
    Ответы сервера: 204 - Чек найден(, 406 - Не найден или сумма(дата) некоректны, 400 - Не указанна дата(сумма)
    """

    # Можно ли здесь код засунуть в один try-except или лучше разделить как сейчас?
    try:
        date_string = receipt_data['t']
        date = datetime.strptime(date_string, '%Y%m%dT%H%M%S')
        format_date = date.strftime('%Y-%m-%dT%H:%M')
        url_check_receipt = 'https://proverkacheka.nalog.ru:9999/v1/ofds/*/inns/*/fss/' + receipt_data['fn'] + \
                            '/operations/' + receipt_data['n'] + '/tickets/' + receipt_data['i'] + '?fiscalSign=' +\
                            receipt_data['fp'] + '&date=' + format_date + '&sum=' + receipt_data['s']
    except KeyError:
        return 'Key Error'

    try:
        check_receipt = requests.get(url_check_receipt)
        status_code = check_receipt.status_code
        text = check_receipt.text
        if status_code != 204:
            return text or 'Empty response'
        else:
            return 'Receipt OK'
    except (requests.RequestException, ValueError):
        return 'Network error'


def get_receipt(receipt_data: dict, login: str, password: int) -> dict:
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
        return {}

    try:
        full_receipt = requests.get(url_receipt, auth=HTTPBasicAuth(login, password), headers=headers)
        full_receipt.raise_for_status()
        data = full_receipt.json()
        return data
    except (requests.RequestException, ValueError):
        return {}
