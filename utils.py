"""Вспомогательные функции ввода."""

from datetime import date


def input_int(prompt: str) -> int:
    """Запросить целое число."""
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("Введите целое число.")


def input_date(prompt: str) -> date:
    """Запросить дату в формате ГГГГ-ММ-ДД."""
    while True:
        try:
            return date.fromisoformat(input(prompt))
        except ValueError:
            print("Введите дату в формате ГГГГ-ММ-ДД.")


def input_text(prompt: str) -> str:
    """Запросить непустую строку."""
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("Введите непустой текст.")
