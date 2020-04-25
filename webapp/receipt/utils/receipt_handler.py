from datetime import datetime
import requests
from requests.auth import HTTPBasicAuth
from typing import Dict
import urllib.parse as urllib

from webapp.db import db
from webapp.receipt.models import Purchase, Receipt


def convert_date_to_fns_format(date_db: datetime) -> str:
    """Convert datetime from database to FNS format"""
    date = date_db.strftime('%Y-%m-%dT%H:%M')
    return date


def format_date(raw_datetime: str) -> datetime:
    """Convert datetime from QR code without 'T' """
    if len(raw_datetime) == 13:  # если в формате не учтены секунды добавляем 00 секунд
        raw_datetime = raw_datetime + '00'
    try:
        date = datetime.strptime(raw_datetime, '%Y%m%dT%H%M%S')
        return date
    except ValueError:
        print('Не возможно распарсить строку datetime')
        return datetime.now()


def purchase_valid_handler(fn_number, receipt_type, fd_number, fpd_number, date, sum):
    """
    Validation receipt function
    Status code:
    204 - Receipt found and valid
    406 - Receipt not found or not valid
    400 - Incorrect date or amount
    :return: status_code, check_receipt.text
    """

    sum = int(float(sum) * 100)
    path = '/v1/ofds/*/inns/*/fss/' + fn_number + '/operations/' + receipt_type + '/tickets/' + fd_number
    query = 'fiscalSign=' + fpd_number + '&date=' + convert_date_to_fns_format(date) + '&sum=' + str(sum)
    par = ('https', 'proverkacheka.nalog.ru:9999', path, '', query, '')
    url_check_receipt = urllib.urlunparse(par)

    try:
        check_receipt = requests.get(url_check_receipt)
        check_receipt.raise_for_status()
        status_code = check_receipt.status_code
        if status_code != 204:
            print('Чек не валиден')
            return status_code, check_receipt.text
        else:
            print('Чек валиден')
            return status_code, check_receipt.text
    except requests.RequestException:
        print('Сетевая ошибка', status_code, check_receipt.text)
        return status_code, check_receipt.text
    except ValueError:
        print('Неверный формат передаваемых данных', status_code, check_receipt.text)
        return status_code, check_receipt.text


def receipt_get_handler(purchase):
    """
    Receive detailed receipt function
    Status code
    200 - return json
    202 - receipt did not pass validation
    204 -
    403 - wrong username or password
    406 - receipt not found
    451 - illegal public api usage
    :return:
    """
    headers = {
        'device-id': '',
        'device-os': '',
    }

    url_receipt = 'https://proverkacheka.nalog.ru:9999/v1/inns/*/kkts/*/fss/' + purchase.fn_number + \
                  '/tickets/' + purchase.fd_number + '?fiscalSign=' + purchase.fpd_number + \
                  '&sendToEmail=no'

    auth_login = purchase.user.fns_login
    auth_password = purchase.user.fns_password
    try:
        full_receipt = requests.get(url_receipt, auth=HTTPBasicAuth(auth_login, auth_password), headers=headers)
        full_receipt.raise_for_status()
        data = full_receipt.json()
        return full_receipt.status_code, data
    except requests.RequestException:
        print('Сетевая ошибка', full_receipt.status_code, full_receipt.text)
        return full_receipt.status_code, full_receipt.text
    except ValueError:
        print('Ошибочное значение', full_receipt.status_code, full_receipt.text)
        return full_receipt.status_code, full_receipt.text


def add_receipt_db():
    """Add detailed information from receipt to database"""
    purchase_list = Purchase.query.filter(Purchase.loaded.is_(None)).all()
    for purchase in purchase_list:
        # проверим чек на валидность. с рез-том ничего не делаем . запрос должен устранить ошибку 451
        check_purchase = purchase_valid_handler(purchase.fn_number, purchase.receipt_type, purchase.fd_number,
                                                purchase.fpd_number, purchase.date, purchase.sum)
        # ecли чек валиден, продолжаем дальше
        if check_purchase[0] != 204:
            print('<Ответ функции проверки валидности: ', check_purchase)
        else:
            # запрашиваем детальную информацию по чеку
            get_purchase = receipt_get_handler(purchase)
            if get_purchase[0] != 200:
                print('<Ответ функции получения детализации по чеку: ', get_purchase)
            else:
                data = get_purchase[1]
                try:
                    organization = data['document']['receipt']['user']
                    purchase.organization = organization
                    purchase.loaded = 'fetched'
                except KeyError:
                    print('Отсутствует название продавца')
                    purchase.organization = 'Продавец не указан'
                    purchase.loaded = 'fetched'
                db.session.add(purchase)
                db.session.commit()
                try:
                    for pozition in data['document']['receipt']['items']:
                        new_receipt = Receipt(purchase_id=purchase.id,
                                              product=pozition['name'],
                                              price=pozition['price'],
                                              quantity=pozition['quantity'],
                                              sum=pozition['sum'],
                                              )
                        db.session.add(new_receipt)
                        db.session.commit()
                except KeyError:
                    print('<Неверные данные в словаре позиций чека')


def registration_fns(email: str, name: str, phone: str) -> str:
    """
    Register user in FNS service
    Status code
    204 - successfully
    400 - invalid email
    409 - user exist,
    500 - invalid phone number,
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
    Recovery password from FNS
    Status code
    204 - successfully,
    404 - user not found
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


def qr_parser(qr_text: str) -> Dict:
    """ Parse data from QR code"""
    receipt_data = {}
    try:
        data = urllib.urlparse(qr_text)
        receipt_params = urllib.parse_qs(data.path, strict_parsing=True)
        for key, values in receipt_params.items():
            receipt_data[key] = values[0]
        #  Из QR кода должны приходить ровно 6 ть параметров
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
