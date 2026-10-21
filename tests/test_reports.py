from pathlib import Path

import pandas as pd
import pytest

from src.reports import save_report, spending_by_category


def test_spending_by_category_filters_dates_and_expenses(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.chdir(tmp_path)
    transactions = pd.DataFrame(
        {
            "Дата операции": pd.to_datetime(
                [
                    "2021-09-19 23:59:59",
                    "2021-09-20 00:00:00",
                    "2021-12-20 23:59:59",
                    "2021-12-21 00:00:00",
                    "2021-11-01 12:00:00",
                    "2021-11-02 12:00:00",
                    "2021-11-03 12:00:00",
                ]
            ),
            "Статус": ["OK", "OK", "OK", "OK", "OK", "FAILED", "OK"],
            "Категория": [
                "Супермаркеты",
                "Супермаркеты",
                "Супермаркеты",
                "Супермаркеты",
                "Супермаркеты",
                "Супермаркеты",
                "Транспорт",
            ],
            "Сумма платежа": [-10, -20, -30, -40, 50, -60, -70],
            "Описание": [
                "до периода",
                "начало",
                "конец",
                "после периода",
                "поступление",
                "ошибка",
                "другая категория",
            ],
        }
    )

    result = spending_by_category(transactions, "Супермаркеты", "2021-12-20")

    assert isinstance(result, pd.DataFrame)
    assert result["Описание"].tolist() == ["начало", "конец"]
    assert len(transactions) == 7

    saved = pd.read_excel(tmp_path / "reports" / "spending_by_category.xlsx")
    assert saved["Описание"].tolist() == ["начало", "конец"]


def test_save_report_accepts_custom_filename(tmp_path: Path) -> None:
    output = tmp_path / "custom.xlsx"

    @save_report(filename=str(output))
    def make_report() -> pd.DataFrame:
        return pd.DataFrame({"amount": [10, 20]})

    result = make_report()

    assert output.is_file()
    pd.testing.assert_frame_equal(pd.read_excel(output), result)
