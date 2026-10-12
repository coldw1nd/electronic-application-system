"""Представления главной страницы и страницы ошибки 404."""

from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

import storage


def index(request: HttpRequest) -> HttpResponse:
    """Показать сводную информацию сервиса."""
    users, statuses, applications = storage.load_data()
    context = {
        "users_count": len(users),
        "statuses_count": len(statuses),
        "applications": applications[:3],
        "applications_count": len(applications),
    }
    return render(request, "homepage/index.html", context)


def page_not_found(
    request: HttpRequest,
    exception: Exception,
) -> HttpResponse:
    """Вернуть страницу ошибки 404."""
    return render(request, "404.html", status=404)
