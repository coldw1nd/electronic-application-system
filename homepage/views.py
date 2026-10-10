"""Представления главной страницы и страницы ошибки 404."""

from html import escape

from django.http import HttpRequest, HttpResponse

import storage


def _page(title: str, content: str) -> str:
    """Сформировать общий HTML-каркас веб-страницы (этап ПР5)."""
    return f'''<!doctype html>
<html lang="ru">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{escape(title)} — Электронные заявления</title>
  <link
href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css"
    rel="stylesheet">
  <style>body {{ background:#f4f7fb; }} .site-header {{ background:#102b4e;
  color:#fff; padding:1.2rem 0; }} .content {{ padding-top:2rem;
  padding-bottom:3rem; }} .card {{ border:0; box-shadow:0 4px 18px #102b4e12;
  margin-bottom:1rem; }} .status {{ border-radius:1rem; padding:.25rem .65rem;
  background:#e5eefb; color:#194d84; }}</style>
</head>
<body>
<header class="site-header"><div class="container">
  <strong>Сервис электронных заявлений</strong>
  <nav class="mt-2 d-flex flex-wrap gap-3">
    <a class="link-light" href="/">Главная</a>
    <a class="link-light" href="/applications/">Заявления</a>
    <a class="link-light" href="/users/">Пользователи</a>
    <a class="link-light" href="/documents/">Документы</a>
  </nav>
</div></header>
<main class="container content">{content}</main>
<footer class="container pb-4 text-secondary small">
  Учебный проект на Django
</footer>
</body></html>'''


def index(request: HttpRequest) -> HttpResponse:
    """Показать главную страницу и основные разделы системы."""
    users, statuses, applications = storage.load_data()
    content = f'''
<section class="p-4 p-md-5 bg-white rounded-4 mb-4">
  <h1 class="display-6">Сервис электронных заявлений</h1>
  <p class="lead">Просмотр заявлений, статусов, документов и комментариев.</p>
  <p class="mb-0">В демонстрационном наборе: {len(applications)} заявлений,
  {len(users)} пользователей и {len(statuses)} статусов.</p>
</section>
<div class="row g-3">
  <div class="col-md-4"><div class="card h-100"><div class="card-body">
    <h2 class="h5">Заявления</h2><p>Список и карточки заявлений.</p>
    <a href="/applications/" class="btn btn-primary">Открыть список</a>
  </div></div></div>
  <div class="col-md-4"><div class="card h-100"><div class="card-body">
    <h2 class="h5">Пользователи</h2><p>Заявители сервиса.</p>
    <a href="/users/" class="btn btn-outline-primary">Открыть список</a>
  </div></div></div>
  <div class="col-md-4"><div class="card h-100"><div class="card-body">
    <h2 class="h5">Документы</h2><p>Файлы, связанные с заявлениями.</p>
    <a href="/documents/" class="btn btn-outline-primary">Открыть список</a>
  </div></div></div>
</div>'''
    return HttpResponse(_page("Главная", content))


def page_not_found(
    request: HttpRequest,
    exception: Exception,
) -> HttpResponse:
    """Вернуть страницу ошибки 404."""
    content = (
        '<section class="bg-white rounded-4 p-5">'
        '<h1>Страница не найдена</h1>'
        '<p>Запрошенный ресурс отсутствует.</p>'
        '<a href="/">Вернуться на главную</a></section>'
    )
    return HttpResponse(_page("404", content), status=404)
