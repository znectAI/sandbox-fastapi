from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_root():
    assert client.get("/").json() == {"message": "hello"}


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_get_item():
    response = client.get("/items/1")
    assert response.status_code == 200
    assert response.json() == {"id": 1, "name": "widget"}


def test_get_item_unknown_returns_404():
    response = client.get("/items/999")
    assert response.status_code == 404
    assert response.json() == {"detail": "not found"}


def test_version():
    response = client.get("/version")
    assert response.status_code == 200
    assert response.json() == {"version": "0.1.0"}


def test_get_item_name():
    response = client.get("/items/1/name")
    assert response.status_code == 200
    assert response.json() == {"name": "widget"}


def test_get_item_name_unknown_returns_404():
    response = client.get("/items/999/name")
    assert response.status_code == 404
    assert response.json() == {"detail": "not found"}


def test_list_items():
    response = client.get("/items")
    assert response.status_code == 200
    body = response.json()
    assert isinstance(body, list)
    assert all(set(item) == {"id", "name"} for item in body)
    assert body == [{"id": 1, "name": "widget"}]


def test_list_items_empty(monkeypatch):
    monkeypatch.setattr("app.main.ITEMS", {})
    response = client.get("/items")
    assert response.status_code == 200
    assert response.json() == []


def test_list_items_sorted_by_name(monkeypatch):
    monkeypatch.setattr(
        "app.main.ITEMS",
        {1: {"id": 1, "name": "b"}, 2: {"id": 2, "name": "a"}},
    )
    assert client.get("/items").json() == [
        {"id": 2, "name": "a"},
        {"id": 1, "name": "b"},
    ]
