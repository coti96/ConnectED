import os
import uuid
import requests


BASE_URL = os.getenv("BASE_URL", "http://localhost:5000")

USER1_EMAIL = os.getenv("TEST_EMAIL", "paul@etudiant.com")
USER1_PASSWORD = os.getenv("TEST_PASSWORD", "password")

USER2_EMAIL = os.getenv("TEST_EMAIL_2", "pro1@company.com")
USER2_PASSWORD = os.getenv("TEST_PASSWORD_2", "password")


def url(path: str) -> str:
    return f"{BASE_URL}{path}"


def login_token(email: str, password: str) -> str:
    r = requests.post(url("/login"), json={"email": email, "password": password}, timeout=10)
    assert r.status_code == 200, r.text
    token = r.json().get("token")
    assert token
    return token


def auth_headers(token: str) -> dict:
    return {"Authorization": f"Bearer {token}"}


def create_project(token: str) -> str:
    title = f"Projet Test Permissions {uuid.uuid4()}"
    payload = {
        "titre": title,
        "description": "Projet de test pour vérifier les permissions API.",
        "domaine": "Santé",
        "nombre_places": 2,
        "deadline": "2026-12-31T00:00:00",
        "technologies": ["Python"],
    }
    r = requests.post(url("/projects"), json=payload, headers=auth_headers(token), timeout=10)
    assert r.status_code == 201, r.text
    pid = r.json().get("id")
    assert pid
    return pid


def test_creator_can_manage_applications_and_others_cannot():
    token1 = login_token(USER1_EMAIL, USER1_PASSWORD)
    token2 = login_token(USER2_EMAIL, USER2_PASSWORD)

    pid = create_project(token1)

    r = requests.get(url(f"/projects/{pid}/applications"), headers=auth_headers(token1), timeout=10)
    assert r.status_code == 200, r.text

    r = requests.get(url(f"/projects/{pid}/applications"), headers=auth_headers(token2), timeout=10)
    assert r.status_code == 403, r.text


def test_cannot_apply_to_own_project():
    token1 = login_token(USER1_EMAIL, USER1_PASSWORD)
    pid = create_project(token1)

    r = requests.post(url(f"/projects/{pid}/apply"), json={}, headers=auth_headers(token1), timeout=10)
    assert r.status_code == 400, r.text


def test_only_creator_can_update_application_status_even_if_application_missing():
    token1 = login_token(USER1_EMAIL, USER1_PASSWORD)
    token2 = login_token(USER2_EMAIL, USER2_PASSWORD)

    pid = create_project(token1)

    r = requests.put(
        url(f"/projects/{pid}/applications/{USER2_EMAIL}/status"),
        json={"status": "REJECTED"},
        headers=auth_headers(token2),
        timeout=10,
    )
    assert r.status_code == 403, r.text

