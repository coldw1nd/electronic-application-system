"""Операции над сущностями сервиса электронных заявлений."""

from datetime import date

from models import Application, Comment, Document, Status, User


def next_id(items: list[object]) -> int:
    """Вернуть следующий свободный идентификатор."""
    if not items:
        return 1
    return max(item.id for item in items) + 1


def find_application(
    applications: list[Application],
    application_id: int,
) -> Application | None:
    """Найти заявление по идентификатору."""
    return next(
        (item for item in applications if item.id == application_id), None
    )


def search_applications(
    applications: list[Application],
    query: str,
) -> list[Application]:
    """Найти заявления по заголовку, описанию или ФИО заявителя."""
    search_text = query.casefold()
    return [
        item for item in applications
        if search_text in item.title.casefold()
        or search_text in item.description.casefold()
        or search_text in item.applicant.full_name.casefold()
    ]


def create_application(
    applications: list[Application],
    users: list[User],
    statuses: list[Status],
    user_id: int,
    title: str,
    description: str,
    created_at: date,
) -> Application:
    """Создать заявление от имени существующего пользователя."""
    user = next((item for item in users if item.id == user_id), None)
    status = next((item for item in statuses if item.name == "Черновик"), None)
    if user is None:
        raise ValueError("Пользователь не найден")
    if status is None:
        raise ValueError("Начальный статус «Черновик» не найден")
    application = Application(
        next_id(applications), title, description, user, status, created_at
    )
    applications.append(application)
    return application


def change_application_status(
    applications: list[Application],
    statuses: list[Status],
    application_id: int,
    status_id: int,
) -> Application:
    """Изменить статус заявления."""
    application = find_application(applications, application_id)
    status = next((item for item in statuses if item.id == status_id), None)
    if application is None:
        raise ValueError("Заявление не найдено")
    if status is None:
        raise ValueError("Статус не найден")
    application.change_status(status)
    return application


def add_document(
    applications: list[Application],
    name: str,
    description: str,
    application_id: int,
    uploaded_at: date,
) -> Document:
    """Добавить документ к заявлению."""
    application = find_application(applications, application_id)
    if application is None:
        raise ValueError("Заявление не найдено")
    all_documents = [doc for app in applications for doc in app.documents]
    document = Document(
        next_id(all_documents), application.id, name, description, uploaded_at
    )
    application.add_document(document)
    return document


def add_comment(
    applications: list[Application],
    users: list[User],
    application_id: int,
    author_id: int,
    text: str,
    created_at: date,
) -> Comment:
    """Добавить комментарий к заявлению от существующего пользователя."""
    application = find_application(applications, application_id)
    author = next((item for item in users if item.id == author_id), None)
    if application is None:
        raise ValueError("Заявление не найдено")
    if author is None:
        raise ValueError("Пользователь не найден")
    all_comments = [
        comment for app in applications for comment in app.comments
    ]
    comment = Comment(
        next_id(all_comments), application.id, author, text, created_at
    )
    application.add_comment(comment)
    return comment
