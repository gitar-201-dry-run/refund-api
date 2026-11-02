import os

import pytest
from fastapi.testclient import TestClient

from app.main import create_app
from app.store_pg import PostgresStore


@pytest.fixture(scope="session")
def database_url() -> str:
    url = os.environ.get("DATABASE_URL")
    if not url:
        pytest.skip("DATABASE_URL is not set")
    return url


@pytest.fixture
def client(database_url: str) -> TestClient:
    return TestClient(create_app(PostgresStore(database_url)))


@pytest.fixture
def charge(client: TestClient) -> dict:
    """A $50.00 charge stored in Postgres."""
    resp = client.post("/charges", json={"amount_cents": 5000, "description": "Order 1042"})
    assert resp.status_code == 201
    return resp.json()
