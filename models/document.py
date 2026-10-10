"""Модель документа, приложенного к заявлению."""

from datetime import date

from models.base import Entity


class Document(Entity):
    """Документ, связанный с конкретным заявлением."""

    def __init__(
        self,
        document_id: int,
        application_id: int,
        name: str,
        description: str,
        uploaded_at: date,
    ) -> None:
        super().__init__(document_id)
        self.application_id = application_id
        self.name = name
        self.description = description
        self.uploaded_at = uploaded_at

    def __str__(self) -> str:
        return f"{self.name} (заявление №{self.application_id})"
