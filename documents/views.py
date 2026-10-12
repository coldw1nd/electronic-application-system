"""Представление списка документов."""

from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

import storage


def index(request: HttpRequest) -> HttpResponse:
    """Показать документы всех заявлений."""
    _, _, applications = storage.load_data()
    documents = [
        {"document": document, "application": application}
        for application in applications
        for document in application.documents
    ]
    return render(request, "documents/index.html", {
        "documents": documents,
    })
