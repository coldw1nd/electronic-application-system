from datetime import date

import pytest

from models import Application, Comment, Document, Status, User


def make_application() -> Application:
    user = User(1, "Анна Иванова", "anna@example.test")
    status = Status(1, "Черновик")
    return Application(
        1, "Справка", "Запрос справки", user, status, date(2026, 10, 1)
    )


def test_application_string_and_status_change() -> None:
    application = make_application()
    assert "Заявление №1" in str(application)
    new_status = Status(2, "На рассмотрении")
    application.change_status(new_status)
    assert application.status is new_status


def test_document_must_belong_to_application() -> None:
    application = make_application()
    document = Document(
        1, 1, "passport.pdf", "Паспорт", date(2026, 10, 1)
    )
    application.add_document(document)
    assert application.documents == [document]
    other_document = Document(
        2, 2, "form.pdf", "Форма", date(2026, 10, 1)
    )
    with pytest.raises(ValueError):
        application.add_document(other_document)


def test_comment_links_author_and_application() -> None:
    application = make_application()
    comment = Comment(
        1, 1, application.applicant, "Принято", date(2026, 10, 2)
    )
    application.add_comment(comment)
    assert application.comments[0].author is application.applicant
    assert "Анна Иванова" in str(comment)


def test_status_final_flag_is_encapsulated() -> None:
    status = Status(3, "Одобрено", is_final=True)
    assert status.is_final is True
    with pytest.raises(AttributeError):
        status.is_final = False
