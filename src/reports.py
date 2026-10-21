import logging
from collections.abc import Callable
from datetime import datetime
from functools import wraps
from pathlib import Path
from typing import Any, TypeVar, cast, overload

import pandas as pd

logger = logging.getLogger(__name__)

F = TypeVar("F", bound=Callable[..., pd.DataFrame])


@overload
def save_report(func: F) -> F: ...


@overload
def save_report(
    func: None = None,
    *,
    filename: str | None = None,
) -> Callable[[F], F]: ...


def save_report(
    func: F | None = None,
    *,
    filename: str | None = None,
) -> F | Callable[[F], F]:
    """Сохраняет DataFrame, возвращённый функцией отчёта, в Excel"""

    def decorate(function: F) -> F:
        @wraps(function)
        def wrapper(*args: Any, **kwargs: Any) -> pd.DataFrame:
            result = function(*args, **kwargs)
            path = Path(filename) if filename is not None else Path("reports") / f"{function.__name__}.xlsx"
            path.parent.mkdir(parents=True, exist_ok=True)
            result.to_excel(path, index=False)
            logger.info("Отчёт сохранён в %s", path)
            return result

        return cast(F, wrapper)

    if func is not None:
        return decorate(func)
    return decorate


@save_report
def spending_by_category(
    transactions: pd.DataFrame,
    category: str,
    date: str | None = None,
) -> pd.DataFrame:
    """Возвращает успешные расходы категории за последние три месяца"""
    report_day = datetime.strptime(date, "%Y-%m-%d").date() if date is not None else datetime.now().date()
    start = pd.Timestamp(report_day) - pd.DateOffset(months=3)
    end = pd.Timestamp(report_day) + pd.Timedelta(days=1)

    mask = (
        transactions["Дата операции"].ge(start)
        & transactions["Дата операции"].lt(end)
        & transactions["Статус"].eq("OK")
        & transactions["Категория"].eq(category)
        & transactions["Сумма платежа"].lt(0)
    )
    result = transactions.loc[mask].copy()
    logger.info("Отчёт по категории %s: %d операций", category, len(result))
    return result
