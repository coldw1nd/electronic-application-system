"""Загрузка и сохранение объектной модели в JSON-файлах."""

import json
from datetime import date
from pathlib import Path
from typing import Any

from models import Application, Comment, Document, Status, User

DATA_DIR = Path(__file__).resolve().parent / "data"


def _read_records(data_dir: Path, filename: str) -> list[dict[str, Any]]:
    path = data_dir / filename
    try:
        with path.open("r", encoding="utf-8") as file:
            records = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []
    return records if isinstance(records, list) else []


def _write_records(
    data_dir: Path,
    filename: str,
    records: list[dict[str, Any]],
) -> None:
    data_dir.mkdir(parents=True, exist_ok=True)
    path = data_dir / filename
    with path.open("w", encoding="utf-8") as file:
        json.dump(records, file, ensure_ascii=False, indent=2)


def _as_date(value: str) -> date:
    return date.fromisoformat(value)


def load_data(
    data_dir: Path = DATA_DIR,
) -> tuple[list[User], list[Status], list[Application]]:
    """Загрузить пользователей, статусы и заявления со связанными объектами."""
    users = [
        User(row["id"], row["full_name"], row["email"])
        for row in _read_records(data_dir, "users.json")
    ]
    statuses = [
        Status(row["id"], row["name"], row.get("is_final", False))
        for row in _read_records(data_dir, "statuses.json")
    ]
    users_by_id = {user.id: user for user in users}
    statuses_by_id = {status.id: status for status in statuses}

    documents_by_application: dict[int, list[Document]] = {}
    for row in _read_records(data_dir, "documents.json"):
        document = Document(
            row["id"],
            row["application_id"],
            row["name"],
            row.get("description", ""),
            _as_date(row["uploaded_at"]),
        )
        documents_by_application.setdefault(
            document.application_id, []
        ).append(document)

    comments_by_application: dict[int, list[Comment]] = {}
    for row in _read_records(data_dir, "comments.json"):
        author = users_by_id.get(row["author_id"])
        if author is None:
            continue
        comment = Comment(
            row["id"],
            row["application_id"],
            author,
            row["text"],
            _as_date(row["created_at"]),
        )
        comments_by_application.setdefault(
            comment.application_id, []
        ).append(comment)

    applications = []
    for row in _read_records(data_dir, "applications.json"):
        applicant = users_by_id.get(row["user_id"])
        status = statuses_by_id.get(row["status_id"])
        if applicant is None or status is None:
            continue
        application = Application(
            row["id"],
            row["title"],
            row["description"],
            applicant,
            status,
            _as_date(row["created_at"]),
        )
        for document in documents_by_application.get(application.id, []):
            application.add_document(document)
        for comment in comments_by_application.get(application.id, []):
            application.add_comment(comment)
        applications.append(application)

    return users, statuses, applications


def save_data(
    users: list[User],
    statuses: list[Status],
    applications: list[Application],
    data_dir: Path = DATA_DIR,
) -> None:
    """Сохранить связанные объекты в пять отдельных JSON-файлов."""
    _write_records(
        data_dir,
        "users.json",
        [
            {"id": user.id, "full_name": user.full_name, "email": user.email}
            for user in users
        ],
    )
    _write_records(
        data_dir,
        "statuses.json",
        [
            {"id": status.id, "name": status.name, "is_final": status.is_final}
            for status in statuses
        ],
    )
    _write_records(
        data_dir,
        "applications.json",
        [
            {
                "id": application.id,
                "title": application.title,
                "description": application.description,
                "user_id": application.applicant.id,
                "status_id": application.status.id,
                "created_at": application.created_at.isoformat(),
            }
            for application in applications
        ],
    )
    _write_records(
        data_dir,
        "documents.json",
        [
            {
                "id": document.id,
                "application_id": document.application_id,
                "name": document.name,
                "description": document.description,
                "uploaded_at": document.uploaded_at.isoformat(),
            }
            for application in applications
            for document in application.documents
        ],
    )
    _write_records(
        data_dir,
        "comments.json",
        [
            {
                "id": comment.id,
                "application_id": comment.application_id,
                "author_id": comment.author.id,
                "text": comment.text,
                "created_at": comment.created_at.isoformat(),
            }
            for application in applications
            for comment in application.comments
        ],
    )
