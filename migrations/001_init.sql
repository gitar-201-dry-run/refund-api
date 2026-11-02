CREATE TABLE charges (
    id           TEXT PRIMARY KEY,
    amount_cents INTEGER NOT NULL CHECK (amount_cents > 0),
    currency     TEXT NOT NULL,
    description  TEXT NOT NULL DEFAULT '',
    created_at   TIMESTAMPTZ NOT NULL
);

CREATE TABLE refunds (
    id           TEXT PRIMARY KEY,
    charge_id    TEXT NOT NULL REFERENCES charges (id),
    amount_cents INTEGER NOT NULL CHECK (amount_cents > 0),
    reason       TEXT,
    created_at   TIMESTAMPTZ NOT NULL
);

CREATE INDEX refunds_charge_id_idx ON refunds (charge_id);
