"""Представления списка пользователей и карточки пользователя."""

from django.http import Http404, HttpRequest, HttpResponse
from django.shortcuts import render

import storage


def index(request: HttpRequest) -> HttpResponse:
    """Показать пользователей системы."""
    users, _, applications = storage.load_data()
    user_rows = [
        {
            "user": user,
            "application_count": sum(
                1 for app in applications if app.applicant.id == user.id
            ),
        }
        for user in users
    ]
    return render(request, "users/index.html", {"user_rows": user_rows})


def detail(request: HttpRequest, user_id: int) -> HttpResponse:
    """Показать пользователя и его заявления."""
    users, _, applications = storage.load_data()
    user = next((item for item in users if item.id == user_id), None)
    if user is None:
        raise Http404("Пользователь не найден")
    user_applications = [
        item for item in applications if item.applicant.id == user.id
    ]
    return render(request, "users/detail.html", {
        "user": user,
        "applications": user_applications,
    })
