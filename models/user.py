"""Модель пользователя сервиса."""

from models.base import Entity


class User(Entity):
    """Пользователь, подающий электронные заявления."""

    def __init__(self, user_id: int, full_name: str, email: str) -> None:
        super().__init__(user_id)
        self.full_name = full_name
        self.email = email

    def __str__(self) -> str:
        return self.full_name
