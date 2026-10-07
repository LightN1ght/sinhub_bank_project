# Обработка банковских данных

## Цель проекта

Проект содержит функции для обработки банковских данных: маскирует номера карт и счетов, формирует подпись для карты или счёта, форматирует дату, фильтрует операции по статусу и сортирует их по дате

## Установка и запуск

Нужен Python 3.14. Скачайте или клонируйте проект и перейдите в его каталог. Дополнительные библиотеки для работы функций не нужны

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

### Тесты и покрытие

Запустить все тесты можно командой:

```bash
pytest
```

Чтобы посмотреть покрытие исходного кода и создать HTML-отчёт в `htmlcov/`, выполните:

```bash
pytest --cov=src --cov-report=term-missing --cov-report=html
```
