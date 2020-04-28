import pytest

from webapp.application import create_app


@pytest.fixture
def app():
    app = create_app()
    return app


def test_landing(client):
    response = client.get("/")
    assert response.status_code == 200