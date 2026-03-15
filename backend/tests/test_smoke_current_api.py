import os
import requests

BASE_URL = os.getenv("BASE_URL", "http://localhost:5000")
TEST_EMAIL = os.getenv("TEST_EMAIL", "paul@etudiant.com")
TEST_PASSWORD = os.getenv("TEST_PASSWORD", "password")


def url(path: str) -> str:
    return f"{BASE_URL}{path}"


def login_token() -> str:
    r = requests.post(url("/login"), json={"email": TEST_EMAIL, "password": TEST_PASSWORD}, timeout=10)
    assert r.status_code == 200, r.text
    token = r.json().get("token")
    assert token
    return token


def auth_headers() -> dict:
    return {"Authorization": f"Bearer {login_token()}"}


def test_login_ok():
    r = requests.post(url("/login"), json={"email": TEST_EMAIL, "password": TEST_PASSWORD}, timeout=10)
    assert r.status_code == 200
    body = r.json()
    assert "token" in body and body["token"]
    assert "user" in body and body["user"].get("email") == TEST_EMAIL


def test_dashboard_requires_auth():
    r = requests.get(url("/dashboard"), timeout=10)
    assert r.status_code in (401, 422)


def test_dashboard_ok():
    r = requests.get(url("/dashboard"), headers=auth_headers(), timeout=10)
    assert r.status_code == 200
    body = r.json()
    assert "stats" in body
    assert "recent_activity" in body
    assert "user" in body and body["user"].get("email") == TEST_EMAIL


def test_projects_list_ok():
    r = requests.get(url("/projects"), timeout=10)
    assert r.status_code == 200
    body = r.json()
    assert "projects" in body and isinstance(body["projects"], list)
    assert len(body["projects"]) > 0
    assert body["projects"][0].get("id")


def test_projects_detail_ok():
    projects = requests.get(url("/projects"), timeout=10).json()["projects"]
    pid = projects[0]["id"]
    r = requests.get(url(f"/projects/{pid}"), timeout=10)
    assert r.status_code == 200
    body = r.json()
    assert "project" in body
    assert body["project"].get("id") == pid


def test_recommended_requires_auth():
    r = requests.get(url("/projects/recommended"), timeout=10)
    assert r.status_code in (401, 422)


def test_recommended_ok_and_has_ids():
    r = requests.get(url("/projects/recommended"), headers=auth_headers(), timeout=10)
    assert r.status_code == 200
    rec = r.json().get("recommendations")
    assert isinstance(rec, list)
    if rec:
        assert rec[0].get("id")


def test_profile_ok():
    r = requests.get(url("/profile"), headers=auth_headers(), timeout=10)
    assert r.status_code == 200
    body = r.json()
    assert body.get("email") == TEST_EMAIL


def test_messages_send_and_fetch():
    r = requests.get(url("/users"), timeout=10)
    assert r.status_code == 200
    users = r.json().get("users")
    assert isinstance(users, list) and users
    other = next((u.get("email") for u in users if u.get("email") and u.get("email") != TEST_EMAIL), None)
    assert other
    payload = {"receiver_email": other, "content": "hello-from-smoke"}
    r = requests.post(url("/messages"), json=payload, headers=auth_headers(), timeout=10)
    assert r.status_code in (201, 200), r.text

    r = requests.get(url("/conversations"), headers=auth_headers(), timeout=10)
    assert r.status_code == 200
    conv = r.json().get("conversations")
    assert isinstance(conv, list)
    assert any(c.get("email") == other for c in conv)

    r = requests.get(url(f"/messages/{other}?limit=20&mark_read=0"), headers=auth_headers(), timeout=10)
    assert r.status_code == 200
    msgs = r.json().get("messages")
    assert isinstance(msgs, list)
    assert any(m.get("content") == "hello-from-smoke" for m in msgs)
