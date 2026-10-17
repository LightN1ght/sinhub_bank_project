from src.transaction_readers import (
    read_transactions_from_csv,
    read_transactions_from_excel,
)
from src.utils import load_transactions
from src.processing import (
    filter_by_state,
    process_bank_search,
    sort_by_date,
)
from src.generators import filter_by_currency
from src.widget import get_date, mask_account_card

def main() -> None:
    """Загружает транзакции, применяет выбранные фильтры и выводит результат"""
    print(
        """
        Программа: Привет! Добро пожаловать в программу работы с банковскими транзакциями.
        Выберите необходимый пункт меню:
        1. Получить информацию о транзакциях из JSON-файла
        2. Получить информацию о транзакциях из CSV-файла
        3. Получить информацию о транзакциях из XLSX-файла
        """
    )

    user_choice = int(input("Пользователь: "))

    if user_choice == 1:
        transactions = load_transactions("data/operations.json")
    elif user_choice == 2:
        transactions = read_transactions_from_csv("data/transactions.csv")
    elif user_choice == 3:
        transactions = read_transactions_from_excel("data/transactions_excel.xlsx")
    else:
        print("Такого пункта нет в меню")
        return

    available_statuses = {"EXECUTED", "CANCELED", "PENDING"}

    while True:
        status = input(
            "Введите статус операции: EXECUTED, CANCELED или PENDING: "
        ).strip().upper()

        if status in available_statuses:
            break

        print(f'Статус операции "{status}" недоступен.')

    filtered_transactions = filter_by_state(transactions, status)

    sort_answer = input("Отсортировать операции по дате? Да/Нет: ").strip().lower()

    if sort_answer == "да":
        direction = input(
            "Введите 1 для сортировки по возрастанию или 2 — по убыванию: "
        ).strip()

        if direction == "1":
            filtered_transactions = sort_by_date(
                filtered_transactions,
                is_reversed=False,
            )
        elif direction == "2":
            filtered_transactions = sort_by_date(
                filtered_transactions,
                is_reversed=True,
            )

    rub_answer = input(
        "Программа: Выводить только рублевые транзакции? Да/Нет: "
    ).strip().lower()

    if rub_answer == "да":
        filtered_transactions = list(
            filter_by_currency(filtered_transactions, "RUB")
        )

    search_answer = input(
        "Отфильтровать операции по слову в описании? Да/Нет: "
    ).strip().lower()

    if search_answer == "да":
        search = input("Введите слово для поиска: ").strip()

        if search:
            filtered_transactions = process_bank_search(
                filtered_transactions,
                search,
            )

    if not filtered_transactions:
        print(
            "Программа: Не найдено ни одной транзакции, "
            "подходящей под ваши условия фильтрации"
        )
        return

    print("Программа: Распечатываю итоговый список транзакций...")
    print(f"Всего банковских операций в выборке: {len(filtered_transactions)}")

    for transaction in filtered_transactions:
        date = get_date(transaction["date"])
        description = transaction["description"]
        sender = transaction.get("from")
        recipient = transaction.get("to")

        if isinstance(sender, str) and sender.strip():
            sender = mask_account_card(sender)
        else:
            sender = ""

        if isinstance(recipient, str) and recipient.strip():
            recipient = mask_account_card(recipient)
        else:
            recipient = ""

        print(f"\n{date} {description}")

        if sender and recipient:
            print(f"{sender} -> {recipient}")
        elif recipient:
            print(recipient)
        elif sender:
            print(sender)
        if "operationAmount" in transaction:
            amount = transaction["operationAmount"]["amount"]
            currency = transaction["operationAmount"]["currency"]["name"]
        else:
            amount = transaction["amount"]
            currency = transaction["currency_name"]

        print(f"Сумма: {amount} {currency}")


if __name__ == "__main__":
    main()
