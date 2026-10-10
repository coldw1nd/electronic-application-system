from datetime import date

import pytest

from models import Application, Status, User
from services import (
    add_comment,
    add_document,
    change_application_status,
    create_application,
    find_application,
    search_applications,
)


def setup_data() -> tuple[list[User], list[Status], list[Application]]:
    users = [User(1, "Анна Иванова", "anna@example.test")]
    statuses = [Status(1, "Черновик"), Status(2, "На рассмотрении")]
    applications = [
        Application(
            1, "Справка", "Запрос справки", users[0], statuses[0],
            date(2026, 10, 1),
        )
    ]
    return users, statuses, applications


def test_search_and_find_application() -> None:
    _, _, applications = setup_data()
    assert find_application(applications, 1) is applications[0]
    assert len(search_applications(applications, "иванова")) == 1
    assert search_applications(applications, "неизвестно") == []


def test_create_application_and_change_status() -> None:
    users, statuses, applications = setup_data()
    created = create_application(
        applications, users, statuses, 1, "Новый запрос",
        "Описание", date(2026, 10, 2),
    )
    assert created.id == 2
    changed = change_application_status(applications, statuses, 2, 2)
    assert changed.status.name == "На рассмотрении"


def test_add_document_and_comment() -> None:
    users, _, applications = setup_data()
    document = add_document(
        applications, "passport.pdf", "Паспорт", 1, date(2026, 10, 2)
    )
    comment = add_comment(
        applications, users, 1, 1, "Принято", date(2026, 10, 2)
    )
    assert applications[0].documents == [document]
    assert applications[0].comments == [comment]


def test_invalid_application_raises() -> None:
    users, statuses, applications = setup_data()
    with pytest.raises(ValueError):
        create_application(
            applications, users, statuses, 99, "Заявление",
            "Текст", date.today(),
        )
