from datetime import datetime


def test_create_charge(client):
    resp = client.post("/charges", json={"amount_cents": 2599, "currency": "USD"})
    assert resp.status_code == 201
    body = resp.json()
    assert body["id"].startswith("ch_")
    assert body["amount_cents"] == 2599
    assert body["currency"] == "usd"


def test_charge_created_at_is_timezone_aware(charge):
    created_at = datetime.fromisoformat(charge["created_at"].replace("Z", "+00:00"))
    assert created_at.tzinfo is not None


def test_get_charge(client, charge):
    resp = client.get(f"/charges/{charge['id']}")
    assert resp.status_code == 200
    assert resp.json()["description"] == "Order 1042"


def test_get_unknown_charge(client):
    assert client.get("/charges/ch_0000000000000000").status_code == 404


def test_rejects_non_positive_amount(client):
    assert client.post("/charges", json={"amount_cents": 0}).status_code == 422


def test_rejects_amount_over_limit(client):
    resp = client.post("/charges", json={"amount_cents": 100_000_01})
    assert resp.status_code == 400
