[![Python 3.6.8](https://img.shields.io/badge/python-3.6.8-green.svg)](https://www.python.org/downloads/release/python-368/)
[![Python 3.11.3](https://img.shields.io/badge/python-3.11.3-green.svg)](https://www.python.org/downloads/release/python-3113/)

[![Maintainability](https://api.codeclimate.com/v1/badges/400d7e960c9264011450/maintainability)](https://codeclimate.com/github/boytsovau/expire_cert_sterra/maintainability)


### Зачем данный скрипт нужен?

    Данный скрипт позволяет получить данные о сроке действия локальных сертификатов на оборудовании S-terra

## Установка

1. Клонируйте репозиторий:

    ```bash
    git clone https://github.com/boytsovau/expire_cert_sterra.git
    cd expire_cert_sterra
    ```

2. Разверните вирутальное окружение:

    ```bash
    python3 -m venv venv
    source /venv/bin/activate
    ```

2. Установите необходимые зависимости:

    ```bash
    pip3 install -r requirements.txt
    ```

### Запуск help

  ```bash
python main.py -h
 ```

### Доступные агрументы

    usage: main.py [-h] --hostname HOSTNAME [HOSTNAME ...] --username USERNAME --password PASSWORD [--port PORT] --command COMMAND [--days DAYS]

    Проверка на срок действия сертификата.

    optional arguments:
    -h, --help            показать это сообщение и выйти
    --hostname HOSTNAME [HOSTNAME ...]
                            список IP адресов
    --username USERNAME   Пользователь для подключения
    --password PASSWORD   Пароль для подключения.
    --port PORT           Порт для подключения (по умолчанию 22).
    --command COMMAND     Команда для выполнения.
    --days DAYS           Дней до конца сертификата. По умолчанию 30.


### Пример использования

    python3 main.py  --hostname 10.10.10.10 10.11.11.11  --username user --password 1234567 --port 22 --command "cert_mgr show" --days 365

    10.10.10.10 

    Сертификат O=TEST,CN=TEST просрочится через 325 дней.

    Данные по сертификату:

    Subject: O=TEST,CN=TEST
    Valid to: Thu Jul 11 13:17:00 2025
    Issuer: C=RU,ST=Moscow,L=Moscow,O=TEST,CN=TEST
    Serial: 11 11 11 11 11 11 11 11 11 11


    10.11.11.11

    Сертификат O=TEST,CN=TEST просрочится через 325 дней.

    Данные по сертификату:

    Subject: O=TEST,CN=TEST
    Valid to: Thu Jul 11 13:17:00 2025
    Issuer: C=RU,ST=Moscow,L=Moscow,O=TEST,CN=TEST
    Serial: 11 11 11 11 11 11 11 11 11 11


## TO DO

1. Реализовать возможность чтения hostname из файла. 
2. Реализовать возможность использовать разные команды для sterra.
3. Реализовать возможность вывода в различные форматы: json, yml
4. Реализовать возможность вывода в файл. 