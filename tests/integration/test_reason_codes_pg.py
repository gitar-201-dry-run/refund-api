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
