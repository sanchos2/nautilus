"""Utils for FNS."""
from datetime import datetime

import requests
from requests.auth import HTTPBasicAuth
from typing import Dict
import urllib.parse as urllib  # noqa: WPS301

from webapp.db import db
from webapp.receipt.models import Purchase, Receipt


def convert_date_to_fns_format(date_db: datetime) -> str:
    """Convert datetime from database to FNS format."""
    return date_db.strftime('%Y-%m-%dT%H:%M')  # noqa: WPS323


def format_date(raw_datetime: str) -> datetime:
    """Convert datetime from QR code without 'T'."""
    # если в формате не учтены секунды добавляем 00 секунд
    if len(raw_datetime) == 13:
        raw_datetime = raw_datetime + '00'  # noqa: WPS336
    try:
        return datetime.strptime(raw_datetime, '%Y%m%dT%H%M%S')  # noqa: WPS323
    except ValueError:
        print('Не возможно распарсить строку datetime')
        return datetime.now().replace(microsecond=0)


def purchase_valid_handler(fn_number, receipt_type, fd_number, fpd_number, date, sum):  # noqa: WPS125, WPS210, WPS211
    """Validate receipt function.

    Status code:
    204 - Receipt found and valid
    406 - Receipt not found or not valid
    400 - Incorrect date or amount

    Args:
        fn_number: from database
        receipt_type: from database
        fd_number: from database
        fpd_number: from database
        date: from database
        sum: from database

    Returns:
         status_code, check_receipt.text.

    """
    sum = int(float(sum) * 100)  # noqa: WPS125
    path = '/v1/ofds/*/inns/*/fss/' + fn_number + '/operations/' + receipt_type + '/tickets/' + fd_number  # noqa: WPS336
    query = 'fiscalSign=' + fpd_number + '&date=' + convert_date_to_fns_format(date) + '&sum=' + str(sum)  # noqa: WPS221, WPS336
    par = ('https', 'proverkacheka.nalog.ru:9999', path, '', query, '')
    url_check_receipt = urllib.urlunparse(par)

    try:
        check_receipt = requests.get(url_check_receipt)
        check_receipt.raise_for_status()
        status_code = check_receipt.status_code
        if status_code != 204:
            print('Чек не валиден')
            return status_code, check_receipt.text
        print('Чек валиден')
        return status_code, check_receipt.text
    except requests.RequestException:
        print('Сетевая ошибка', status_code, check_receipt.text)
        return status_code, check_receipt.text
    except ValueError:
        print(
            'Неверный формат передаваемых данных',
            status_code,
            check_receipt.text,
        )
        return status_code, check_receipt.text


def receipt_get_handler(purchase):  # noqa: WPS210
    """Receive detailed receipt function.

    Status code
    200 - return json
    202 - receipt did not pass validation
    204 -
    403 - wrong username or password
    406 - receipt not found
    451 - illegal public api usage

    Args:
        purchase: purchase data from database query.

    Returns:
        status code, text.

    """
    headers = {
        'device-id': '',
        'device-os': '',
    }

    url_receipt = 'https://proverkacheka.nalog.ru:9999/v1/inns/*/kkts/*/fss/'\
                  + purchase.fn_number + '/tickets/' + purchase.fd_number \
                  + '?fiscalSign=' + purchase.fpd_number + '&sendToEmail=no'  # noqa: WPS336

    auth_login = purchase.user.fns_login
    auth_password = purchase.user.fns_password
    try:
        full_receipt = requests.get(
            url_receipt,
            auth=HTTPBasicAuth(auth_login, auth_password),
            headers=headers,
        )
        full_receipt.raise_for_status()
        full_receipt_data = full_receipt.json()
        return full_receipt.status_code, full_receipt_data
    except requests.RequestException:
        print('Сетевая ошибка', full_receipt.status_code, full_receipt.text)
        return full_receipt.status_code, full_receipt.text
    except ValueError:
        print(
            'Ошибочное значение',
            full_receipt.status_code,
            full_receipt.text,
        )
        return full_receipt.status_code, full_receipt.text


def add_receipt_db():  # noqa: WPS210, WPS231
    """Add detailed information from receipt to database."""
    purchase_list = Purchase.query.filter(Purchase.loaded.is_(None)).all()
    for purchase in purchase_list:
        # проверим чек на валидность. с рез-том ничего не делаем.
        # запрос должен устранить ошибку 451
        check_purchase = purchase_valid_handler(
            purchase.fn_number,
            purchase.receipt_type,
            purchase.fd_number,
            purchase.fpd_number,
            purchase.date,
            purchase.sum,
        )
        # ecли чек валиден, продолжаем дальше
        if check_purchase[0] != 204:  # noqa: WPS504
            print('<Ответ функции проверки валидности: ', check_purchase)
        else:
            # запрашиваем детальную информацию по чеку
            get_purchase = receipt_get_handler(purchase)
            if get_purchase[0] != 200:  # noqa: WPS504
                print(
                    '<Ответ функции получения детализации по чеку: ',
                    get_purchase,
                )
            else:
                receipt_data = get_purchase[1]
                try:
                    organization = receipt_data['document']['receipt']['user']
                    purchase.organization = organization
                    purchase.loaded = 'fetched'
                except KeyError:
                    print('Отсутствует название продавца')
                    purchase.organization = 'Продавец не указан'
                    purchase.loaded = 'fetched'
                db.session.add(purchase)
                db.session.commit()
                try:
                    for pos in receipt_data['document']['receipt']['items']:
                        new_receipt = Receipt(  # noqa: WPS220
                            purchase_id=purchase.id,
                            product=pos['name'],
                            price=pos['price'],
                            quantity=pos['quantity'],
                            sum=pos['sum'],
                        )
                        db.session.add(new_receipt)  # noqa: WPS220
                        db.session.commit()  # noqa: WPS220
                except KeyError:
                    print('<Неверные данные в словаре позиций чека')


def registration_fns(email: str, name: str, phone: str) -> str:
    """Register user in FNS service.

    Status code
    204 - successfully
    400 - invalid email
    409 - user exist,
    500 - invalid phone number.

    Args:
        email: email
        name: nickname
        phone: phone number

    Returns:
        str.

    """
    registration_url = 'https://proverkacheka.nalog.ru:9999/v1/mobile/users/signup'
    registration_data = {
        'email': email,
        'name': name,
        'phone': phone
    }
    try:
        registration_request = requests.post(
            registration_url,
            json=registration_data,
        )
        status_code = registration_request.status_code
        text = registration_request.text
        if status_code != 204:
            return text
        return 'Регистрация успешна'
    except requests.RequestException:
        return 'Сетевая ошибка'
    except ValueError:
        return 'Пользователь уже создан или неправильный телефон / email'


def recovery_pass(phone: str) -> str:  # noqa: WPS231
    """Recovery password from FNS.

    Status code
    204 - successfully,
    404 - user not found

    Args:
        phone: phone number.

    Returns:
        str.

    """
    recovery_url = 'https://proverkacheka.nalog.ru:9999/v1/mobile/users/restore'
    if len(phone) != 12:  # noqa: WPS504
        return 'Не верное количество цифр в номере телефона'
    else:
        phone_data = {'phone': phone}
        try:
            recovery_request = requests.post(recovery_url, json=phone_data)
            status_code = recovery_request.status_code
            text = recovery_request.text
            if status_code != 204:
                return text
            return 'Запрос на восстановления пароля выполнен успешно. Ожидайте СМС'
        except requests.RequestException:
            return 'Сетевая ошибка'
        except ValueError:
            return 'Незарегистрированная учетная запись'


def qr_parser(qr_text: str) -> Dict:
    """Parse data from QR code."""
    receipt_data = {}
    try:
        parse_data = urllib.urlparse(qr_text)
    except AttributeError:
        print('QR код передан не в строковом формате')
        return {}
    try:
        receipt_params = urllib.parse_qs(parse_data.path, strict_parsing=True)
    except ValueError:
        print('Информация в QR коде не в формате параметр=значение')
        return {}
    try:
        for receipt_key, receipt_value in receipt_params.items():
            receipt_data[receipt_key] = receipt_value[0]
        #  Из QR кода должны приходить ровно 6 ть параметров
        assert len(receipt_data) == 6  # noqa: S101
    except AssertionError:
        print('Количество параметров в QR коде не верное')
        return {}
    return receipt_data
