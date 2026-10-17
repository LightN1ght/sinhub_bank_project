import main as app


def set_user_answers(monkeypatch, answers):
    answers_iterator = iter(answers)
    monkeypatch.setattr("builtins.input", lambda _prompt="": next(answers_iterator))


def test_main_json_filters_and_displays_transaction(monkeypatch, capsys):
    transactions = [
        {
            "state": "EXECUTED",
            "date": "2024-03-11T02:26:18.671407",
            "description": "Перевод организации",
            "operationAmount": {
                "amount": "100.00",
                "currency": {"name": "руб.", "code": "RUB"},
            },
            "from": "Visa Classic 1234567890123456",
            "to": "Счет 40817810099910004321",
        },
        {
            "state": "EXECUTED",
            "date": "2024-03-10T02:26:18.671407",
            "description": "Перевод с карты на карту",
            "operationAmount": {
                "amount": "20.00",
                "currency": {"name": "USD", "code": "USD"},
            },
        },
        {
            "state": "CANCELED",
            "date": "2024-03-09T02:26:18.671407",
            "description": "Перевод организации",
            "operationAmount": {
                "amount": "30.00",
                "currency": {"name": "руб.", "code": "RUB"},
            },
        },
    ]
    monkeypatch.setattr(app, "load_transactions", lambda _path: transactions)
    set_user_answers(
        monkeypatch,
        ["1", "invalid", "executed", "да", "1", "да", "да", "ПЕРЕВОД"],
    )

    app.main()

    output = capsys.readouterr().out
    assert 'Статус операции "INVALID" недоступен.' in output
    assert "Всего банковских операций в выборке: 1" in output
    assert "11.03.2024 Перевод организации" in output
    assert "Visa Classic 1234 56** **** 3456 -> Счет **4321" in output
    assert "Сумма: 100.00 руб." in output


def test_main_reads_csv_and_displays_sender_only(monkeypatch, capsys):
    transaction = {
        "state": "CANCELED",
        "date": "2024-03-11T02:26:18",
        "description": "Перевод организации",
        "amount": 250,
        "currency_name": "руб.",
        "currency_code": "RUB",
        "from": "Visa Classic 1234567890123456",
    }
    monkeypatch.setattr(
        app,
        "read_transactions_from_csv",
        lambda _path: [transaction],
    )
    set_user_answers(monkeypatch, ["2", "canceled", "да", "2", "нет", "нет"])

    app.main()

    output = capsys.readouterr().out
    assert "Visa Classic 1234 56** **** 3456" in output
    assert " -> " not in output
    assert "Сумма: 250 руб." in output


def test_main_reads_excel_and_displays_recipient_only(monkeypatch, capsys):
    transaction = {
        "state": "PENDING",
        "date": "2024-03-11T02:26:18",
        "description": "Открытие вклада",
        "amount": 500,
        "currency_name": "руб.",
        "currency_code": "RUB",
        "to": "Счет 40817810099910004321",
    }
    monkeypatch.setattr(
        app,
        "read_transactions_from_excel",
        lambda _path: [transaction],
    )
    set_user_answers(monkeypatch, ["3", "PENDING", "нет", "нет", "нет"])

    app.main()

    output = capsys.readouterr().out
    assert "Счет **4321" in output
    assert " -> " not in output
    assert "Сумма: 500 руб." in output


def test_main_handles_empty_result(monkeypatch, capsys):
    monkeypatch.setattr(app, "load_transactions", lambda _path: [])
    set_user_answers(monkeypatch, ["1", "EXECUTED", "нет", "нет", "нет"])

    app.main()

    assert "Не найдено ни одной транзакции" in capsys.readouterr().out


def test_main_handles_unknown_menu_item(monkeypatch, capsys):
    set_user_answers(monkeypatch, ["9"])

    app.main()

    assert "Такого пункта нет в меню" in capsys.readouterr().out
