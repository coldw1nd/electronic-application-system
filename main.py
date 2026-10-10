"""Консольный интерфейс для проверки объектной модели ПР3."""

from datetime import date

import services
import storage
import utils
from models import Application, Status, User


def show_applications(applications: list[Application]) -> None:
    """Показать список электронных заявлений."""
    if not applications:
        print("Заявления не найдены.")
        return
    for application in applications:
        print(application)
        print(f"   Заявитель: {application.applicant}")
        print(f"   Дата: {application.created_at:%d.%m.%Y}")
        print(f"   Документов: {len(application.documents)}")
        print(f"   Комментариев: {len(application.comments)}")


def choose_user(users: list[User]) -> int:
    """Вывести пользователей и получить идентификатор."""
    for user in users:
        print(f"{user.id}. {user.full_name} ({user.email})")
    return utils.input_int("ID пользователя: ")


def choose_status(statuses: list[Status]) -> int:
    """Вывести статусы и получить идентификатор."""
    for status in statuses:
        print(f"{status.id}. {status.name}")
    return utils.input_int("ID статуса: ")


def main() -> None:
    """Запустить меню консольного приложения."""
    users, statuses, applications = storage.load_data()
    while True:
        print("\n=== Сервис электронных заявлений ===")
        print("1. Показать заявления")
        print("2. Найти заявление")
        print("3. Создать заявление")
        print("4. Изменить статус")
        print("5. Добавить документ")
        print("6. Добавить комментарий")
        print("0. Сохранить и выйти")
        action = utils.input_int("Действие: ")
        try:
            if action == 1:
                show_applications(applications)
            elif action == 2:
                query = utils.input_text("Поисковый запрос: ")
                found = services.search_applications(applications, query)
                show_applications(found)
            elif action == 3:
                user_id = choose_user(users)
                title = utils.input_text("Название заявления: ")
                description = utils.input_text("Описание: ")
                result = services.create_application(
                    applications, users, statuses, user_id, title, description,
                    date.today(),
                )
                print(f"Создано: {result}")
            elif action == 4:
                application_id = utils.input_int("ID заявления: ")
                status_id = choose_status(statuses)
                print(services.change_application_status(
                    applications, statuses, application_id, status_id
                ))
            elif action == 5:
                application_id = utils.input_int("ID заявления: ")
                name = utils.input_text("Название документа: ")
                description = utils.input_text("Описание документа: ")
                result = services.add_document(
                    applications, name, description, application_id,
                    date.today(),
                )
                print(f"Добавлен документ: {result}")
            elif action == 6:
                application_id = utils.input_int("ID заявления: ")
                author_id = choose_user(users)
                text = utils.input_text("Комментарий: ")
                result = services.add_comment(
                    applications, users, application_id, author_id, text,
                    date.today(),
                )
                print(f"Добавлен комментарий: {result}")
            elif action == 0:
                storage.save_data(users, statuses, applications)
                print("Данные сохранены.")
                break
            else:
                print("Неизвестный пункт меню.")
        except ValueError as error:
            print(f"Ошибка: {error}")


if __name__ == "__main__":
    main()
