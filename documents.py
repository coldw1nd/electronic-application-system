"""Функции работы с документами."""

from datetime import date, timedelta


def next_id(items: list[dict]) -> int:
    """Вернуть следующий идентификатор."""
    if not items:
        return 1
    return max(item["id"] for item in items) + 1


def add_document(
    documents: list[dict],
    title: str,
    author: str,
    created_at: date,
    days_for_approval: int,
) -> dict:
    """Добавить документ и вернуть его."""
    due_date = created_at + timedelta(days=days_for_approval)
    document = {
        "id": next_id(documents),
        "title": title,
        "author": author,
        "created_at": created_at.isoformat(),
        "due_date": due_date.isoformat(),
        "is_ready": True,
    }
    documents.append(document)
    return document


def find_documents(
    documents: list[dict],
    query: str,
) -> list[dict]:
    """Найти документы по названию или автору."""
    query = query.lower()
    result = []
    for document in documents:
        title = document["title"].lower()
        author = document["author"].lower()
        if query in title or query in author:
            result.append(document)
    return result


def get_document_by_id(
    documents: list[dict],
    document_id: int,
) -> dict | None:
    """Найти документ по идентификатору."""
    for document in documents:
        if document["id"] == document_id:
            return document
    return None


def sort_documents(documents: list[dict]) -> list[dict]:
    """Отсортировать документы по названию."""
    return sorted(documents, key=lambda document: document["title"])
