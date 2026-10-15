"""API behaviour tests."""
from tests.conftest import login, auth


def test_home_ok(client):
    res = client.get("/")
    assert res.status_code == 200
    assert res.json()["service"] == "SecureNotes API"


def test_register_then_login(client):
    reg = client.post("/register", json={"username": "carol", "password": "carolpass"})
    assert reg.status_code == 200

    res = client.post("/login", json={"username": "carol", "password": "carolpass"})
    assert res.status_code == 200
    assert res.json()["access_token"].count(".") == 2


def test_login_wrong_password_is_401(client):
    res = client.post("/login", json={"username": "alice", "password": "WRONG"})
    assert res.status_code == 401


def test_create_then_list_own_note(client):
    alice = login(client, "alice", "alicepass")

    created = client.post(
        "/notes", json={"title": "Groceries", "body": "milk, eggs"}, headers=auth(alice)
    )
    assert created.status_code == 200

    listed = client.get("/notes", headers=auth(alice))
    assert listed.status_code == 200
    assert "Groceries" in [n["title"] for n in listed.json()]
