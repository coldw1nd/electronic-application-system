"""Модель статуса заявления."""

from models.base import Entity


class Status(Entity):
    """Состояние обработки заявления."""

    def __init__(
        self, status_id: int, name: str, is_final: bool = False
    ) -> None:
        super().__init__(status_id)
        self.name = name
        self._is_final = bool(is_final)

    @property
    def is_final(self) -> bool:
        """Признак конечного статуса (только чтение)."""
        return self._is_final

    def __str__(self) -> str:
        return self.name
