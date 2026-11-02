ALTER TABLE refunds ADD COLUMN reason_code TEXT
    CHECK (reason_code IN ('duplicate', 'fraudulent', 'requested_by_customer', 'other'));
