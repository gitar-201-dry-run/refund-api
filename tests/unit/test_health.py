from fastapi.testclient import TestClient

from app.main import create_app
from app.store import MemoryStore


def test_health():
    client = TestClient(create_app(MemoryStore()))
    assert client.get("/health").json() == {"status": "ok"}
