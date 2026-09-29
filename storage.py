"""Функции загрузки и сохранения данных проекта."""

import json
from pathlib import Path


def load_json(filename: str) -> list[dict]:
    """Загрузить список словарей из JSON-файла."""
    try:
        with open(filename, encoding="utf-8") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def save_json(filename: str, items: list[dict]) -> None:
    """Сохранить список словарей в JSON-файл."""
    Path(filename).parent.mkdir(exist_ok=True)
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(items, file, ensure_ascii=False, indent=2)
