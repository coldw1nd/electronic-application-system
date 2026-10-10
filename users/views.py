"""Представления списка пользователей и карточки пользователя."""

from html import escape

from django.http import Http404, HttpRequest, HttpResponse

import storage
from homepage.views import _page


def index(request: HttpRequest) -> HttpResponse:
    """Показать пользователей системы."""
    users, _, applications = storage.load_data()
    content = ['<h1 class="mb-4">Пользователи</h1>', '<div class="row g-3">']
    for user in users:
        count = sum(1 for app in applications if app.applicant.id == user.id)
        content.append(
            f'<div class="col-md-6"><article class="card">'
            f'<div class="card-body"><h2 class="h5">'
            f'<a href="/users/{user.id}/">{escape(user.full_name)}</a>'
            f'</h2><p>{escape(user.email)}</p>'
            f'<p class="mb-0">Заявлений: {count}</p>'
            f'</div></article></div>'
        )
    content.append('</div>')
    return HttpResponse(_page("Пользователи", "\n".join(content)))


def detail(request: HttpRequest, user_id: int) -> HttpResponse:
    """Показать пользователя и его заявления."""
    users, _, applications = storage.load_data()
    user = next((item for item in users if item.id == user_id), None)
    if user is None:
        raise Http404("Пользователь не найден")
    content = [
        f'<h1>{escape(user.full_name)}</h1>',
        f'<p>Электронная почта: {escape(user.email)}</p>',
        '<h2 class="h4 mt-4">Заявления пользователя</h2>',
    ]
    user_applications = [
        item for item in applications if item.applicant.id == user.id
    ]
    if not user_applications:
        content.append('<p>У пользователя пока нет заявлений.</p>')
    for application in user_applications:
        content.append(
            f'<p><a href="/applications/{application.id}/">'
            f'{escape(application.title)}</a> — '
            f'{escape(application.status.name)}</p>'
        )
    return HttpResponse(_page(user.full_name, "\n".join(content)))
