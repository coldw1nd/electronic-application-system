"""Представления списка заявлений и карточки заявления."""

from django.http import Http404, HttpRequest, HttpResponse
from django.shortcuts import render

import storage


def index(request: HttpRequest) -> HttpResponse:
    """Показать все заявления."""
    _, _, applications = storage.load_data()
    return render(request, "applications/index.html", {
        "applications": applications,
    })


def detail(request: HttpRequest, application_id: int) -> HttpResponse:
    """Показать заявление, документы и комментарии."""
    _, _, applications = storage.load_data()
    application = next(
        (item for item in applications if item.id == application_id), None
    )
    if application is None:
        raise Http404("Заявление не найдено")
    return render(request, "applications/detail.html", {
        "application": application,
    })
