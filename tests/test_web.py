from django.test import Client, override_settings


@override_settings(DEBUG=False)
def test_main_routes_return_successful_responses() -> None:
    client = Client()
    paths = [
        "/",
        "/applications/",
        "/applications/1/",
        "/users/",
        "/users/1/",
        "/documents/",
    ]
    for path in paths:
        response = client.get(path)
        assert response.status_code == 200, path


@override_settings(DEBUG=False)
def test_documents_page_displays_document_and_application() -> None:
    response = Client().get("/documents/")

    assert response.status_code == 200
    html = response.content.decode("utf-8")
    assert "passport.pdf" in html
    assert "Копия паспорта заявителя" in html
    assert "Заявление на выдачу справки" in html
    assert 'href="/applications/1/"' in html
    assert "f'Заявление на выдачу справки" not in html


@override_settings(DEBUG=False)
def test_unknown_application_returns_404() -> None:
    response = Client().get("/applications/9999/")
    assert response.status_code == 404
