"""Общий базовый класс сущностей предметной области."""


class Entity:
    """Базовая сущность с идентификатором."""

    def __init__(self, entity_id: int) -> None:
        self.id = entity_id

    def __str__(self) -> str:
        return f"{type(self).__name__} #{self.id}"
