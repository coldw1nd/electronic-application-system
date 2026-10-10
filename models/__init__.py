"""Объектная модель сервиса электронных заявлений."""

from models.application import Application
from models.comment import Comment
from models.document import Document
from models.status import Status
from models.user import User

__all__ = ["Application", "Comment", "Document", "Status", "User"]
