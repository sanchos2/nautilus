import pytest

from webapp.application import create_app


@pytest.fixture
def app():
    app = create_app()
    return app


def test_admin(client):
    response = client.get("/admin")
    assert response.status_code == 308


def test_category_add(client):
    response = client.get("/admin/category-add")
    assert response.status_code == 405


def test_subcategory_add(client):
    response = client.get("/admin/category-add")
    assert response.status_code == 405
