"""Функции работы с комментариями."""


def next_id(items: list[dict]) -> int:
    """Вернуть следующий идентификатор."""
    if not items:
        return 1
    return max(item["id"] for item in items) + 1


def add_comment(
    comments: list[dict],
    document_id: int,
    author: str,
    text: str,
) -> dict:
    """Добавить комментарий."""
    comment = {
        "id": next_id(comments),
        "document_id": document_id,
        "author": author,
        "text": text,
    }
    comments.append(comment)
    return comment


def find_comments(
    comments: list[dict],
    document_id: int,
) -> list[dict]:
    """Найти комментарии документа."""
    result = []
    for comment in comments:
        if comment["document_id"] == document_id:
            result.append(comment)
    return result
