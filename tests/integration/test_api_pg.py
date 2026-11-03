"""API tests against a real Postgres. Run scripts/migrate.py first."""


def test_create_and_fetch_charge(client, charge):
    resp = client.get(f"/charges/{charge['id']}")
    assert resp.status_code == 200
    body = resp.json()
    assert body["id"] == charge["id"]
    assert body["amount_cents"] == 5000
    assert body["description"] == "Order 1042"


def test_fetch_unknown_charge(client):
    assert client.get("/charges/ch_0000000000000000").status_code == 404


def test_full_refund(client, charge):
    resp = client.post(f"/charges/{charge['id']}/refund")
    assert resp.status_code == 201
    body = resp.json()
    assert body["id"].startswith("re_")
    assert body["charge_id"] == charge["id"]
    assert body["amount_cents"] == 5000


def test_refund_shows_in_refund_list(client, charge):
    client.post(f"/charges/{charge['id']}/refund")
    refunds = client.get(f"/charges/{charge['id']}/refunds").json()
    assert [r["amount_cents"] for r in refunds] == [5000]


def test_charge_cannot_be_fully_refunded_twice(client, charge):
    assert client.post(f"/charges/{charge['id']}/refund").status_code == 201
    assert client.post(f"/charges/{charge['id']}/refund").status_code == 409


def test_reason_code_is_stored_and_listed(client, charge):
    resp = client.post(f"/charges/{charge['id']}/refund", json={"reason_code": "requested_by_customer"})
    assert resp.status_code == 201
    assert resp.json()["reason_code"] == "requested_by_customer"
    refunds = client.get(f"/charges/{charge['id']}/refunds").json()
    assert [r["reason_code"] for r in refunds] == ["requested_by_customer"]


def test_unknown_reason_code_returns_422(client, charge):
    resp = client.post(f"/charges/{charge['id']}/refund", json={"reason_code": "nope"})
    assert resp.status_code == 422
    assert client.get(f"/charges/{charge['id']}/refunds").json() == []
