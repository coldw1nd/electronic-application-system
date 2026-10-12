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
def test_unknown_application_returns_404() -> None:
    response = Client().get("/applications/9999/")
    assert response.status_code == 404
