"""
Tests for registration, login, and JWT-protected access.

These exercise the business rules in services/auth_service.py - duplicate
email handling, credential verification, and token validation - rather than
FastAPI/Pydantic's own request-parsing behavior.
"""


def test_register_returns_user_without_password(client, user_a_credentials):
    response = client.post("/register", json=user_a_credentials)

    assert response.status_code == 201
    body = response.json()
    assert body["email"] == user_a_credentials["email"]
    assert body["name"] == user_a_credentials["name"]
    # The password hash must never be exposed in the API response.
    assert "password" not in body
    assert "password_hash" not in body


def test_register_duplicate_email_is_rejected(client, user_a_credentials):
    client.post("/register", json=user_a_credentials)

    # Same email, different name - the duplicate check is on email alone.
    duplicate = client.post(
        "/register",
        json={**user_a_credentials, "name": "Someone Else"},
    )

    assert duplicate.status_code == 409


def test_login_with_correct_credentials_returns_token(client, user_a_credentials):
    client.post("/register", json=user_a_credentials)

    response = client.post(
        "/login",
        json={"email": user_a_credentials["email"], "password": user_a_credentials["password"]},
    )

    assert response.status_code == 200
    body = response.json()
    assert body["token_type"] == "bearer"
    assert len(body["access_token"]) > 0


def test_login_with_wrong_password_is_rejected(client, user_a_credentials):
    client.post("/register", json=user_a_credentials)

    response = client.post(
        "/login",
        json={"email": user_a_credentials["email"], "password": "wrong-password"},
    )

    assert response.status_code == 401


def test_profile_rejects_invalid_token(client):
    response = client.get(
        "/profile", headers={"Authorization": "Bearer this-is-not-a-real-jwt"}
    )

    assert response.status_code == 401


def test_profile_returns_current_user_with_valid_token(client, auth_headers, user_a_credentials):
    response = client.get("/profile", headers=auth_headers)

    assert response.status_code == 200
    assert response.json()["email"] == user_a_credentials["email"]


def test_register_rejects_password_over_bcrypt_byte_limit(client):
    # 100 ASCII characters = 100 bytes: under the schema's max_length=128
    # character cap, but over bcrypt's 72-byte hashing limit. Before the
    # fix, this reached bcrypt directly and crashed with a 500
    # (ValueError: password cannot be longer than 72 bytes); it must now
    # fail as a clean validation error instead.
    response = client.post(
        "/register",
        json={"name": "Alice", "email": "alice@example.com", "password": "a" * 100},
    )

    assert response.status_code == 422
    assert "72 bytes" in response.text


def test_register_accepts_password_at_bcrypt_byte_limit(client):
    # Exactly 72 bytes must still succeed - the check is "over the limit",
    # not "at or over".
    response = client.post(
        "/register",
        json={"name": "Alice", "email": "alice@example.com", "password": "a" * 72},
    )

    assert response.status_code == 201
