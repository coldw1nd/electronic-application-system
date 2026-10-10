"""Представление списка документов."""

from html import escape

from django.http import HttpRequest, HttpResponse

import storage
from homepage.views import _page


def index(request: HttpRequest) -> HttpResponse:
    """Показать документы всех заявлений."""
    _, _, applications = storage.load_data()
    content = ['<h1 class="mb-4">Документы</h1>']
    documents = [
        (document, application)
        for application in applications
        for document in application.documents
    ]
    if not documents:
        content.append('<p>Документы не найдены.</p>')

    for document, application in documents:
        content.append(
            f'<article class="card"><div class="card-body">'
            f'<h2 class="h5">{escape(document.name)}</h2>'
            f'<p>{escape(document.description)}</p>'
            f'<p class="mb-0">Заявление: '
            f'<a href="/applications/{application.id}/">'
            f'{escape(application.title)}</a> · дата загрузки: '
            f'{document.uploaded_at:%d.%m.%Y}</p>'
            f'</div></article>'
        )

    return HttpResponse(_page("Документы", "\n".join(content)))
