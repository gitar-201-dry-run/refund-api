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


def test_refund_with_reason_code(client, charge):
    resp = client.post(f"/charges/{charge['id']}/refund", json={"reason_code": "duplicate"})
    assert resp.status_code == 201
    assert resp.json()["reason_code"] == "duplicate"


def test_refund_without_reason_code(client, charge):
    resp = client.post(f"/charges/{charge['id']}/refund")
    assert resp.status_code == 201
    assert resp.json()["reason_code"] is None


def test_refund_rejects_unsupported_reason_code(client, charge):
    resp = client.post(f"/charges/{charge['id']}/refund", json={"reason_code": "unsupported"})
    assert resp.status_code == 422


def test_refund_with_unknown_reason_code_is_rejected(client, charge):
    resp = client.post(f"/charges/{charge['id']}/refund", json={"reason_code": "bogus"})
    assert resp.status_code == 422
    assert client.get(f"/charges/{charge['id']}/refunds").json() == []


def test_reason_code_appears_in_refund_list(client, charge):
    client.post(f"/charges/{charge['id']}/refund", json={"reason_code": "fraudulent"})
    refunds = client.get(f"/charges/{charge['id']}/refunds").json()
    assert [r["reason_code"] for r in refunds] == ["fraudulent"]
