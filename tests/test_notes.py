import pytest
from fastapi.testclient import TestClient

from app.database import initialize_database
from app.main import app


@pytest.fixture()
def client(tmp_path, monkeypatch):
    database_file = tmp_path / "test_notes.db"

    monkeypatch.setattr(
        "app.database.DATABASE_PATH",
        database_file,
    )

    initialize_database()

    with TestClient(app) as test_client:
        yield test_client


def test_create_note(client):
    response = client.post(
        "/notes",
        json={"title": "First note", "content": "Hello"},
    )
    assert response.status_code == 201
    assert response.json()["title"] == "First note"


def test_list_notes(client):
    client.post(
        "/notes",
        json={"title": "First note", "content": "Hello"},
    )
    response = client.get("/notes")
    assert response.status_code == 200
    assert len(response.json()) == 1


def test_get_missing_note(client):
    response = client.get("/notes/999")
    assert response.status_code == 404
    assert response.json()["success"] is False


def test_update_note(client):
    created = client.post(
        "/notes",
        json={"title": "Old", "content": "Old content"},
    )
    note_id = created.json()["id"]

    response = client.put(
        f"/notes/{note_id}",
        json={"title": "New", "content": "New content"},
    )

    assert response.status_code == 200
    assert response.json()["title"] == "New"


def test_delete_note(client):
    created = client.post(
        "/notes",
        json={"title": "Temporary", "content": "Delete me"},
    )
    note_id = created.json()["id"]

    response = client.delete(f"/notes/{note_id}")
    assert response.status_code == 200
    assert client.get(f"/notes/{note_id}").status_code == 404


def test_reject_blank_title(client):
    response = client.post(
        "/notes",
        json={"title": "   ", "content": "Hello"},
    )
    assert response.status_code == 400


def test_reject_blank_content(client):
    response = client.post(
        "/notes",
        json={"title": "Valid title", "content": "   "},
    )
    assert response.status_code == 400


def test_reject_malformed_json(client):
    response = client.post(
        "/notes",
        content='{"title": ',
        headers={"Content-Type": "application/json"},
    )
    assert response.status_code == 400