import pytest
from fastapi.testclient import TestClient

from app.main import create_app
from app.store import MemoryStore


@pytest.fixture
def client() -> TestClient:
    return TestClient(create_app(MemoryStore()))


@pytest.fixture
def charge(client: TestClient) -> dict:
    """A $50.00 charge."""
    resp = client.post("/charges", json={"amount_cents": 5000, "description": "Order 1042"})
    assert resp.status_code == 201
    return resp.json()
