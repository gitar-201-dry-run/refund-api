# Refund API

A small payments API: create charges, refund them. Amounts are integer cents.

## Run it

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## Endpoints

| Method | Path | What it does |
|---|---|---|
| POST | `/charges` | Create a charge |
| GET | `/charges/{id}` | Fetch a charge |
| POST | `/charges/{id}/refund` | Refund a charge in full |
| GET | `/charges/{id}/refunds` | List refunds for a charge |

### Refund reason codes

`POST /charges/{id}/refund` takes an optional JSON body with a `reason_code`. The allowed values are `duplicate`, `fraudulent`, `requested_by_customer`, and `other`. Any other value is rejected with a 422 and no refund is created. The code is stored with the refund and returned as `reason_code` by the refund and list endpoints.

```bash
curl -X POST localhost:8000/charges/$CHARGE_ID/refund \
  -H 'content-type: application/json' \
  -d '{"reason_code": "duplicate"}'
```

Storage is in memory unless `DATABASE_URL` is set, in which case the API uses Postgres. In-memory data resets when the server restarts.

## Test

```bash
pytest -q tests/unit
```

Unit tests run against the in-memory store. See Postgres below for the integration tests.

## Postgres

```bash
export DATABASE_URL=postgresql://postgres:postgres@localhost:5432/refunds
python scripts/migrate.py
pytest -q tests/integration
```

## CI

`.github/workflows/ci.yml` runs four checks on every pull request: `lint` (ruff), `unit-tests`, `integration-tests (postgres)`, and `docker-build` (build the image and call `/health`).
