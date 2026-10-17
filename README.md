# Обработка банковских данных

## Цель проекта

Проект содержит функции для обработки банковских данных: маскирует номера карт и счетов, формирует подпись для карты или счёта, форматирует дату, фильтрует и сортирует операции, загружает транзакции из JSON-, CSV- и Excel-файлов и конвертирует суммы в USD и EUR в рубли.
## Установка и запуск

Нужен Python 3.14. Скачайте или клонируйте проект и перейдите в его каталог. Установите зависимости командой:

```bash
poetry install
```

Для конвертации транзакций в USD и EUR создайте `.env` на основе шаблона и укажите API-ключ Exchange Rates Data:

```bash
cp .env.example .env
```

Добавьте в `.env` свой ключ:

```env
EXCHANGE_API=ваш_api_ключ
```

Для транзакций в рублях API-ключ не требуется.

Запустить демонстрационную программу можно командой:

```bash
python main.py
```

Программа попросит ввести номер карты и номер счёта, после чего покажет их маскированные версии

## Использование функций

Импортируйте нужные функции из пакетов `src` и передайте им данные.

### Маскирование карты и счёта

```python
from src.masks import get_mask_card_number, get_mask_account

get_mask_card_number("1234567812345678")  # '1234 56** **** 5678'
get_mask_account("40817810099910004312")  # '**4312'
```

### Подпись карты или счёта и форматирование даты

```python
from src.widget import mask_account_card, get_date

mask_account_card("Visa Platinum 1234567812345678")  # 'Visa Platinum 1234 56** **** 5678'
mask_account_card("Счет 40817810099910004312")       # 'Счет **4312'
get_date("2024-03-11T02:26:18.671407")               # '11.03.2024'
```

### Фильтрация и сортировка операций

Каждая операция передаётся как словарь с ключами `state` и `date`. Фильтр по умолчанию оставляет операции со статусом `EXECUTED`; сортировка по умолчанию располагает их от новых к старым. Чтобы отсортировать от старых к новым, передайте `is_reversed=False`.

```python
from src.processing import filter_by_state, sort_by_date

operations = [
    {"state": "EXECUTED", "date": "2024-03-11T02:26:18.671407"},
    {"state": "PENDING", "date": "2024-03-12T10:00:00"},
    {"state": "EXECUTED", "date": "2024-03-08T12:30:00"},
]

completed = filter_by_state(operations)
latest_first = sort_by_date(completed)
oldest_first = sort_by_date(completed, is_reversed=False)
```

### Генераторы для транзакций и номеров карт

Модуль `src.generators` содержит генераторы для отбора транзакций по коду валюты, получения описаний операций и выдачи номеров карт в диапазоне.

```python
from src.generators import (
    card_number_generator,
    filter_by_currency,
    transaction_descriptions,
)

transactions = [
    {
        "id": 1,
        "description": "Перевод организации",
        "operationAmount": {
            "amount": "9824.07",
            "currency": {"name": "USD", "code": "USD"},
        },
    },
    {
        "id": 2,
        "description": "Перевод со счета на счет",
        "operationAmount": {
            "amount": "5000.00",
            "currency": {"name": "руб.", "code": "RUB"},
        },
    },
]

# Генератор возвращает только транзакции с указанным кодом валюты.
usd_transactions = list(filter_by_currency(transactions, "USD"))

# Генератор выдаёт описания в порядке исходного списка.
descriptions = list(transaction_descriptions(transactions))

# Границы диапазона включены; номера форматируются группами по четыре цифры.
card_numbers = list(card_number_generator(1, 3))
# ['0000 0000 0000 0001', '0000 0000 0000 0002', '0000 0000 0000 0003']
```

### Логирование вызовов функций

Модуль `src.decorators` содержит декоратор `log`. Он записывает начало вызова функции и сообщение об успешном завершении. Если функция завершается ошибкой, в лог попадают её имя, тип ошибки и переданные аргументы. После записи ошибка передаётся дальше.

Если `filename` не указан, сообщения выводятся в консоль. Если указан, они дописываются в файл.

```python
from src.decorators import log


@log()
def add(x, y):
    return x + y


@log(filename="mylog.txt")
def divide(x, y):
    return x / y


add(1, 2)
divide(10, 2)
```

### Загрузка транзакций из JSON

Модуль `src.utils` содержит функцию `load_transactions`. Она принимает путь к JSON-файлу и возвращает список транзакций. Если файл не найден, пустой, содержит некорректный JSON или данные верхнего уровня не являются списком, функция возвращает пустой список.

Файл с операциями проекта находится в `data/operations.json`.

```python
from src.utils import load_transactions

transactions = load_transactions("data/operations.json")
```

### Конвертация суммы в рубли

Модуль `src.external_api` содержит функцию `convert_to_rub`. Она принимает словарь с данными одной транзакции и возвращает её сумму в рублях типа `float`. Для RUB сумма возвращается без обращения к API. Для USD и EUR используется Exchange Rates Data API и ключ из `.env`.

```python
from src.external_api import convert_to_rub

transaction = {
    "operationAmount": {
        "amount": "10",
        "currency": {"name": "USD", "code": "USD"},
    },
}

amount_in_rubles = convert_to_rub(transaction)
print(amount_in_rubles)
```

Для конвертации USD и EUR нужны настроенный API-ключ и подключение к интернету.

### Чтение транзакций из CSV и Excel

Модуль `src.transaction_readers` содержит функции для чтения транзакций из CSV- и Excel-файлов. Каждая функция принимает путь к файлу и возвращает список словарей: один словарь на строку таблицы. В CSV-файле значения разделены точкой с запятой.

```python
from src.transaction_readers import (
    read_transactions_from_csv,
    read_transactions_from_excel,
)

csv_transactions = read_transactions_from_csv("data/transactions.csv")
excel_transactions = read_transactions_from_excel(
    "data/transactions_excel.xlsx"
)

print(csv_transactions[0])
print(excel_transactions[0])
```

### Тесты и покрытие

Запустить все тесты можно командой:

```bash
pytest
```

Чтобы посмотреть покрытие исходного кода и создать HTML-отчёт в `htmlcov/`, выполните:

```bash
pytest --cov=src --cov-report=term-missing --cov-report=html
```
