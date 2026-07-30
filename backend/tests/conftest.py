"""
Shared pytest fixtures for the LinkFlow backend test suite.

Test database strategy:
- We use an in-memory SQLite database instead of a real Postgres instance.
  This keeps the suite fast, deterministic, and runnable with zero external
  setup (no Docker/Postgres required to run `pytest`).
- SQLite in-memory DBs are normally per-connection (i.e. each new connection
  gets a *different*, empty database). We use `StaticPool` to force every
  connection in the test process to share the same single in-memory DB, so
  the app's requests and the test's own assertions see the same data.
- Required settings (DATABASE_URL, JWT_SECRET_KEY) must be set *before*
  `core.config.settings` is first imported, since it's instantiated once at
  module import time - hence these env vars are set at the very top of this
  file, before any application import.
"""

import os

os.environ.setdefault("DATABASE_URL", "sqlite:///:memory:")
os.environ.setdefault("JWT_SECRET_KEY", "test-secret-key-do-not-use-in-production")
os.environ.setdefault("CORS_ORIGINS", "http://localhost:5173")

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from database.session import Base, get_db
from main import app

# A single shared connection/engine for the whole test run - StaticPool is
# what makes "in-memory" actually shared across the app's requests instead
# of each `get_db()` call seeing a fresh, empty database.
test_engine = create_engine(
    "sqlite:///:memory:",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)


def _override_get_db():
    db = TestSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = _override_get_db


@pytest.fixture(autouse=True)
def _fresh_database():
    """
    Recreate all tables before every test and drop them after.

    This is what makes tests isolated and deterministic - no test can leak
    state (a user, a URL) into another test, regardless of run order.
    """
    Base.metadata.create_all(bind=test_engine)
    yield
    Base.metadata.drop_all(bind=test_engine)


@pytest.fixture
def client():
    """A TestClient wired to the app with the test DB override in place."""
    with TestClient(app) as c:
        yield c


@pytest.fixture
def user_a_credentials():
    return {"name": "Alice", "email": "alice@example.com", "password": "password123"}


@pytest.fixture
def user_b_credentials():
    return {"name": "Bob", "email": "bob@example.com", "password": "password456"}


@pytest.fixture
def user_a_token(client, user_a_credentials):
    """Registers user A and returns a valid JWT access token for them."""
    client.post("/register", json=user_a_credentials)
    response = client.post(
        "/login",
        json={"email": user_a_credentials["email"], "password": user_a_credentials["password"]},
    )
    return response.json()["access_token"]


@pytest.fixture
def user_b_token(client, user_b_credentials):
    """Registers user B and returns a valid JWT access token for them - used
    to test that one user can't act on another user's resources."""
    client.post("/register", json=user_b_credentials)
    response = client.post(
        "/login",
        json={"email": user_b_credentials["email"], "password": user_b_credentials["password"]},
    )
    return response.json()["access_token"]


@pytest.fixture
def auth_headers(user_a_token):
    return {"Authorization": f"Bearer {user_a_token}"}


@pytest.fixture
def other_user_auth_headers(user_b_token):
    return {"Authorization": f"Bearer {user_b_token}"}
