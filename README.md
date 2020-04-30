# NAUTILUS
# Сервис контроля за личными расходами.

[![wemake-python-styleguide](https://img.shields.io/badge/style-wemake-000000.svg)](https://github.com/wemake-services/wemake-python-styleguide)
[![Build Status](https://travis-ci.org/sanchos2/nautilus.svg?branch=master)](https://travis-ci.org/sanchos2/nautilus)
[![codecov](https://codecov.io/gh/sanchos2/nautilus/branch/master/graph/badge.svg)](https://codecov.io/gh/sanchos2/nautilus)
![Python package](https://github.com/sanchos2/nautilus/workflows/Python%20package/badge.svg)


[Демо версия сервиса](https://nautilus.com.ru) 



## Требования

- [PostgreSQL 10](https://www.postgresql.org/)
- [uWSGI](https://uwsgi-docs.readthedocs.io/en/latest/) или [Gunicorn](https://gunicorn.org/)
- [Nginx](https://nginx.org/)
- [Supervisor](http://supervisord.org/)
- Python 3.7 и выше


## Установка

Установка Python 3.7 и необходимых пакетов (применительно к Ubuntu 18.04)
```bash
sudo apt install python3.7
sudo apt install python3-pip python3.7-dev build-essential libssl-dev libffi-dev python3-setuptools python3.7-venv
```

Устанавливаем poetry
```bash
pip install poetry
```

Клонируем проект
```bash
git clone https://github.com/sanchos2/nautilus.git
```
Переходим в папку проекта, устанавливаем зависимости и активируем виртуальное окружение
```bash
cd ./nautilus/
poetry install
```
В файле config.yaml в разделе PRODUCTION необходимо указать необходимые данные:
- SQLALCHEMY_DATABASE_URI: 'postgresql://user:password@ip_address:5432/database'
- SECRET_KEY: 'super_secret_key'

Обновить базу данных
```bash
poetry run flask db upgrade
```

Запусть файл create_admin.py и создать пользователя с правами администратора
```bash
poetry run python create_admin.py
```
Внести изменения в файл /webapp/templates/receipt/qrscaner.html
```
fetch('http://ip_address_your_server/api/v1/qrscaner-process')
```

## Настройка
Создать задачу для supervisor c параметром
```
celery -A tasks worker -B --loglevel=INFO
```
#### Настроить uWSGI или Gunicorn
#### Настроить Nginx

#### Done!

