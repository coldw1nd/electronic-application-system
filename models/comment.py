"""Модель комментария к заявлению."""

from datetime import date

from models.base import Entity
from models.user import User


class Comment(Entity):
    """Комментарий пользователя к заявлению."""

    def __init__(
        self,
        comment_id: int,
        application_id: int,
        author: User,
        text: str,
        created_at: date,
    ) -> None:
        super().__init__(comment_id)
        self.application_id = application_id
        self.author = author
        self.text = text
        self.created_at = created_at

    def __str__(self) -> str:
        return f"{self.author}: {self.text}"
