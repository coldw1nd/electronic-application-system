"""Модель электронного заявления."""

from datetime import date

from models.base import Entity
from models.comment import Comment
from models.document import Document
from models.status import Status
from models.user import User


class Application(Entity):
    """Заявление пользователя со статусом, документами и комментариями."""

    def __init__(
        self,
        application_id: int,
        title: str,
        description: str,
        applicant: User,
        status: Status,
        created_at: date,
        documents: list[Document] | None = None,
        comments: list[Comment] | None = None,
    ) -> None:
        super().__init__(application_id)
        self.title = title
        self.description = description
        self.applicant = applicant
        self.status = status
        self.created_at = created_at
        self.documents = list(documents or [])
        self.comments = list(comments or [])

    def change_status(self, status: Status) -> None:
        """Установить новый статус заявления."""
        self.status = status

    def add_document(self, document: Document) -> None:
        """Добавить документ, относящийся к этому заявлению."""
        if document.application_id != self.id:
            raise ValueError("Документ относится к другому заявлению")
        self.documents.append(document)

    def add_comment(self, comment: Comment) -> None:
        """Добавить комментарий, относящийся к этому заявлению."""
        if comment.application_id != self.id:
            raise ValueError("Комментарий относится к другому заявлению")
        self.comments.append(comment)

    def __str__(self) -> str:
        return f"Заявление №{self.id}: {self.title} ({self.status.name})"
