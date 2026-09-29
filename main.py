"""Точка запуска консольного приложения."""

from datetime import date

import approvals
import comments
import documents
import storage
import utils

DOCUMENTS_FILE = "data/documents.json"
APPROVALS_FILE = "data/approvals.json"
COMMENTS_FILE = "data/comments.json"


def show_documents(document_list: list[dict]) -> None:
    """Вывести документы."""
    if not document_list:
        print("Документы не найдены")
        return

    today = date.today()
    for document in documents.sort_documents(document_list):
        left = approvals.days_left(document, today)
        status = approvals.get_approval_status(left)
        print(f"{document['id']}. {document['title']}")
        print(f"   Автор: {document['author']}")
        print(f"   Срок: {document['due_date']}")
        print(f"   Статус: {status}")


def show_approvals(approval_list: list[dict]) -> None:
    """Вывести согласования."""
    if not approval_list:
        print("Согласования не найдены")
        return

    for approval in approval_list:
        print(f"{approval['id']}. Документ {approval['document_id']}")
        print(f"   Согласующий: {approval['approver']}")
        print(f"   Согласовано: {approval['approved']}")

    approved_count = 0
    for _ in approvals.approved_approvals(approval_list):
        approved_count += 1
    print(f"Согласовано: {approved_count}")


def show_comments(comment_list: list[dict]) -> None:
    """Вывести комментарии."""
    if not comment_list:
        print("Комментарии не найдены")
        return

    for comment in comment_list:
        print(f"{comment['id']}. Документ {comment['document_id']}")
        print(f"   {comment['author']}: {comment['text']}")


def add_document_action(document_list: list[dict]) -> None:
    """Добавить документ."""
    title = utils.input_text("Название документа: ")
    author = utils.input_text("Автор: ")
    created_at = utils.input_date("Дата создания ГГГГ-ММ-ДД: ")
    days = utils.input_int("Срок согласования в днях: ")
    document = documents.add_document(
        document_list,
        title,
        author,
        created_at,
        days,
    )
    print(f"Документ создан: id={document['id']}")


def find_documents_action(document_list: list[dict]) -> None:
    """Найти документы."""
    query = utils.input_text("Поиск: ")
    found = documents.find_documents(document_list, query)
    show_documents(found)


def create_approval_action(
    approval_list: list[dict],
    document_list: list[dict],
) -> None:
    """Создать согласование."""
    document_id = utils.input_int("Id документа: ")
    document = documents.get_document_by_id(
        document_list,
        document_id,
    )
    if document is None:
        print("Документ не найден")
        return

    approver = utils.input_text("Согласующий: ")
    level = utils.input_int("Уровень полномочий: ")
    approval = approvals.create_approval(
        approval_list,
        document_id,
        approver,
        level,
    )
    if approval is None:
        print("Недостаточно полномочий")
        return

    print(f"Согласование создано: id={approval['id']}")


def approve_action(
    approval_list: list[dict],
    document_list: list[dict],
) -> None:
    """Согласовать документ."""
    approval_id = utils.input_int("Id согласования: ")
    result = approvals.approve_document(
        approval_list,
        document_list,
        approval_id,
        date.today(),
    )
    print(result)


def add_comment_action(comment_list: list[dict]) -> None:
    """Добавить комментарий."""
    document_id = utils.input_int("Id документа: ")
    author = utils.input_text("Автор комментария: ")
    text = utils.input_text("Текст комментария: ")
    comment = comments.add_comment(
        comment_list,
        document_id,
        author,
        text,
    )
    print(f"Комментарий добавлен: id={comment['id']}")


def main() -> None:
    """Запустить меню приложения."""
    document_list = storage.load_json(DOCUMENTS_FILE)
    approval_list = storage.load_json(APPROVALS_FILE)
    comment_list = storage.load_json(COMMENTS_FILE)

    while True:
        print("=== Система согласования документов ===")
        print("1. Показать документы")
        print("2. Добавить документ")
        print("3. Найти документ")
        print("4. Показать согласования")
        print("5. Назначить согласующего")
        print("6. Согласовать документ")
        print("7. Показать комментарии")
        print("8. Добавить комментарий")
        print("0. Выход")

        action = utils.input_int("Выберите действие: ")
        if action == 1:
            show_documents(document_list)
        elif action == 2:
            add_document_action(document_list)
        elif action == 3:
            find_documents_action(document_list)
        elif action == 4:
            show_approvals(approval_list)
        elif action == 5:
            create_approval_action(approval_list, document_list)
        elif action == 6:
            approve_action(approval_list, document_list)
        elif action == 7:
            show_comments(comment_list)
        elif action == 8:
            add_comment_action(comment_list)
        elif action == 0:
            break
        else:
            print("Неизвестное действие")

    storage.save_json(DOCUMENTS_FILE, document_list)
    storage.save_json(APPROVALS_FILE, approval_list)
    storage.save_json(COMMENTS_FILE, comment_list)


if __name__ == "__main__":
    main()
