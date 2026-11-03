def test_refund_with_reason_code(client, charge):
    resp = client.post(f"/charges/{charge['id']}/refund", json={"reason_code": "duplicate"})
    assert resp.status_code == 201
    assert resp.json()["reason_code"] == "duplicate"


def test_refund_without_reason_code(client, charge):
    resp = client.post(f"/charges/{charge['id']}/refund")
    assert resp.status_code == 201
    assert resp.json()["reason_code"] is None


def test_reason_code_appears_in_refund_list(client, charge):
    client.post(f"/charges/{charge['id']}/refund", json={"reason_code": "fraudulent"})
    refunds = client.get(f"/charges/{charge['id']}/refunds").json()
    assert [r["reason_code"] for r in refunds] == ["fraudulent"]
