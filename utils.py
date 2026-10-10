"""Вспомогательные функции для консольного интерфейса."""


def input_int(prompt: str) -> int:
    """Запрашивать целое число до корректного ввода."""
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("Введите целое число.")


def input_text(prompt: str) -> str:
    """Запрашивать непустой текст."""
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("Поле не должно быть пустым.")
