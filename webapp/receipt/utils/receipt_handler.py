import requests
from requests.auth import HTTPBasicAuth
import urllib.parse as urllib

from webapp.db import db
from webapp.receipt.models import Receipt, Purchase


"""протестировать функцию т.к. возможны проблемы с сервером налоговой!!!"""


def convert_date_to_fns_format(date_db):
    date = date_db.strftime('%Y-%m-%dT%H:%M')
    return date


def receipt_get_handler():
    receipt = Purchase.query.filter(Purchase.loaded.isnot('fetched')).all()
    for items in receipt:
        headers = {
            'device-id': '',
            'device-os': '',
        }
        # headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:74.0) Gecko/20100101 Firefox/74.0'}
        try:
            url_receipt = 'https://proverkacheka.nalog.ru:9999/v1/inns/*/kkts/*/fss/' + items.fn_number + \
                          '/tickets/' + items.fd_number + '?fiscalSign=' + items.fpd_number + \
                          '&sendToEmail=no'
        except KeyError:
            print('Неизвестный ключ словаря')

        try:
            auth_login = items.user.fns_login
            auth_password = items.user.fns_password
            full_receipt = requests.get(url_receipt, auth=HTTPBasicAuth(auth_login, auth_password), headers=headers)
            full_receipt.raise_for_status()
            data = full_receipt.json()
            if data:
                if not Receipt.query.filter(Receipt.purchase_id == items.id).count() > 0:
                    try:
                        organization = data['document']['receipt']['user']
                        items.organization = organization
                        items.loaded = 'fetched'
                    except KeyError:
                        print('Отсутствует название продавца')
                        items.organization = 'Продавец не указан'
                        items.loaded = 'fetched'
                    db.session.add(items)
                    db.session.commit()
                    for pozition in data['document']['receipt']['items']:
                        new_receipt = Receipt(purchase_id=items.id,
                                              product=pozition['name'],
                                              price=pozition['price'],
                                              quantity=pozition['quantity'],
                                              sum=pozition['sum'],
                                              )
                        db.session.add(new_receipt)
                        db.session.commit()
                else:
                    print('Полные данные по чеку уже внесены')
        except requests.RequestException:
            print('Сетевая ошибка',full_receipt.status_code, full_receipt.text)
        except ValueError:
            print(full_receipt.status_code, full_receipt.text)


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