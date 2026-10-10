"""Представления списка заявлений и карточки заявления."""

from html import escape

from django.http import Http404, HttpRequest, HttpResponse

import storage
from homepage.views import _page


def index(request: HttpRequest) -> HttpResponse:
    """Показать все заявления."""
    _, _, applications = storage.load_data()
    content = ['<h1 class="mb-4">Электронные заявления</h1>']
    if not applications:
        content.append('<p class="alert alert-light">Заявлений пока нет.</p>')
    for application in applications:
        content.append(
            f'<article class="card"><div class="card-body">'
            f'<h2 class="h5"><a href="/applications/{application.id}/">'
            f'{escape(application.title)}</a></h2>'
            f'<p>{escape(application.description)}</p>'
            f'<p class="mb-0">Заявитель: '
            f'{escape(application.applicant.full_name)} · '
            f'<span class="status">{escape(application.status.name)}</span>'
            f'</p></div></article>'
        )
    return HttpResponse(_page("Заявления", "\n".join(content)))


def detail(request: HttpRequest, application_id: int) -> HttpResponse:
    """Показать заявление, документы и комментарии."""
    _, _, applications = storage.load_data()
    application = next(
        (item for item in applications if item.id == application_id), None
    )
    if application is None:
        raise Http404("Заявление не найдено")
    content = [
        f'<h1>{escape(application.title)}</h1>',
        f'<p>{escape(application.description)}</p>',
        f'<p>Заявитель: {escape(application.applicant.full_name)}</p>',
        f'<p>Дата создания: {application.created_at:%d.%m.%Y}</p>',
        f'<p>Статус: <span class="status">'
        f'{escape(application.status.name)}</span></p>',
        '<h2 class="h4 mt-4">Документы</h2>',
    ]
    if application.documents:
        content.append('<ul>')
        for document in application.documents:
            content.append(
                f'<li>{escape(document.name)} — '
                f'{escape(document.description)}</li>'
            )
        content.append('</ul>')
    else:
        content.append('<p>Документы не приложены.</p>')
    content.append('<h2 class="h4 mt-4">Комментарии</h2>')
    if application.comments:
        for comment in application.comments:
            content.append(
                f'<p><strong>{escape(comment.author.full_name)}:</strong> '
                f'{escape(comment.text)}</p>'
            )
    else:
        content.append('<p>Комментариев пока нет.</p>')
    content.append('<a href="/applications/">К списку заявлений</a>')
    return HttpResponse(_page(application.title, "\n".join(content)))
