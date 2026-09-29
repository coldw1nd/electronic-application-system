"""Функции работы с согласованиями."""

from collections.abc import Iterator
from datetime import date

from documents import get_document_by_id


def get_due_date(document: dict) -> date:
    """Вернуть дату окончания согласования."""
    return date.fromisoformat(document["due_date"])


def days_left(document: dict, today: date) -> int:
    """Вернуть число оставшихся дней."""
    return (get_due_date(document) - today).days


def get_approval_status(days_left_value: int) -> str:
    """Вернуть статус согласования."""
    if days_left_value < 0:
        return "Срок согласования истёк"
    if days_left_value <= 2:
        return "Срочное согласование"
    return "Стандартное согласование"


def can_approve(document: dict, today: date) -> bool:
    """Проверить возможность согласования."""
    return document["is_ready"] and days_left(document, today) >= 0


def can_assign_approver(approver_level: int) -> bool:
    """Проверить уровень полномочий согласующего."""
    return approver_level >= 2


def next_id(items: list[dict]) -> int:
    """Вернуть следующий идентификатор."""
    if not items:
        return 1
    return max(item["id"] for item in items) + 1


def create_approval(
    approvals: list[dict],
    document_id: int,
    approver: str,
    approver_level: int,
) -> dict | None:
    """Создать согласование, если хватает полномочий."""
    if not can_assign_approver(approver_level):
        return None
    approval = {
        "id": next_id(approvals),
        "document_id": document_id,
        "approver": approver,
        "approver_level": approver_level,
        "approved": False,
        "approved_at": None,
    }
    approvals.append(approval)
    return approval


def get_approval_by_id(
    approvals: list[dict],
    approval_id: int,
) -> dict | None:
    """Найти согласование по идентификатору."""
    for approval in approvals:
        if approval["id"] == approval_id:
            return approval
    return None


def approve_document(
    approvals: list[dict],
    documents: list[dict],
    approval_id: int,
    today: date,
) -> str:
    """Согласовать документ."""
    approval = get_approval_by_id(approvals, approval_id)
    if approval is None:
        return "Согласование не найдено"

    document = get_document_by_id(documents, approval["document_id"])
    if document is None:
        return "Документ не найден"

    if approval["approved"]:
        return "Документ уже согласован"

    if not can_approve(document, today):
        return "Согласование недоступно"

    approval["approved"] = True
    approval["approved_at"] = today.isoformat()
    return "Документ согласован"


def approved_approvals(
    approvals: list[dict],
) -> Iterator[dict]:
    """Вернуть только согласованные согласования."""
    for approval in approvals:
        if approval["approved"]:
            yield approval
