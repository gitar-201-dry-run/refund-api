from fastapi.testclient import TestClient

from app.main import create_app
from app.store import MemoryStore


def test_full_refund(client, charge):
    resp = client.post(f"/charges/{charge['id']}/refund")
    assert resp.status_code == 201
    body = resp.json()
    assert body["id"].startswith("re_")
    assert body["amount_cents"] == 5000
    assert body["charge_id"] == charge["id"]


def test_full_refund_shows_in_refund_list(client, charge):
    client.post(f"/charges/{charge['id']}/refund")
    refunds = client.get(f"/charges/{charge['id']}/refunds").json()
    assert [r["amount_cents"] for r in refunds] == [5000]


def test_charge_cannot_be_fully_refunded_twice(client, charge):
    client.post(f"/charges/{charge['id']}/refund")
    resp = client.post(f"/charges/{charge['id']}/refund")
    assert resp.status_code == 409


def test_refund_unknown_charge(client):
    assert client.post("/charges/ch_0000000000000000/refund").status_code == 404


def test_list_refunds_unknown_charge(client):
    assert client.get("/charges/ch_0000000000000000/refunds").status_code == 404


def test_refund_summary_uses_injected_store(monkeypatch):
    store = MemoryStore()
    client = TestClient(create_app(store))
    charge = client.post("/charges", json={"amount_cents": 5000, "description": "Order 1042"}).json()
    calls = []

    def refund_totals(charge_id):
        calls.append(charge_id)
        return 2, 1250

    monkeypatch.setattr(store, "refund_totals", refund_totals)

    body = client.get(f"/charges/{charge['id']}/refund-summary").json()

    assert calls == [charge["id"]]
    assert (body["refund_count"], body["refunded_cents"], body["remaining_cents"]) == (2, 1250, 3750)


def test_refund_summary_before_any_refund(client, charge):
    body = client.get(f"/charges/{charge['id']}/refund-summary").json()
    assert body == {
        "charge_id": charge["id"],
        "refund_count": 0,
        "refunded_cents": 0,
        "remaining_cents": 5000,
    }


def test_refund_summary_after_full_refund(client, charge):
    client.post(f"/charges/{charge['id']}/refund")
    body = client.get(f"/charges/{charge['id']}/refund-summary").json()
    assert body["refund_count"] == 1
    assert body["refunded_cents"] == 5000
    assert body["remaining_cents"] == 0


def test_refund_summary_unknown_charge(client):
    assert client.get("/charges/ch_0000000000000000/refund-summary").status_code == 404
