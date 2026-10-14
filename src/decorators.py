from collections.abc import Callable
from datetime import datetime
from functools import wraps
from typing import ParamSpec, TypeVar

P = ParamSpec("P")
R = TypeVar("R")


def log(
    filename: str | None = None,
) -> Callable[[Callable[P, R]], Callable[P, R]]:
    """Создаёт декоратор для записи результата вызова функции"""
    def decorator(func: Callable[P, R]) -> Callable[P, R]:
        """Оборачивает функцию логированием"""
        @wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            """Записывает начало вызова, результат или сведения об ошибке"""
            started_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            message = f"{started_at} {func.__name__} started"

            if filename is None:
                print(message)
            else:
                with open(filename, "a", encoding="utf-8") as file:
                    file.write(message + "\n")

            try:
                result = func(*args, **kwargs)
            except Exception as error:
                message = (
                    f"{func.__name__} error: {type(error).__name__}. "
                    f"Inputs: {args}, {kwargs}"
                )
                if filename is None:
                    print(message)
                else:
                    with open(filename, "a", encoding="utf-8") as file:
                        file.write(message + "\n")
                raise
            else:
                message = f"{func.__name__} ok"
                if filename is None:
                    print(message)
                else:
                    with open(filename, "a", encoding="utf-8") as file:
                        file.write(message + "\n")
                return result

        return wrapper

    return decorator