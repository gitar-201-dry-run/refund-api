from dataclasses import dataclass, field
from datetime import datetime, timezone


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


@dataclass
class Charge:
    id: str
    amount_cents: int
    currency: str
    description: str
    created_at: datetime = field(default_factory=utc_now)


@dataclass
class Refund:
    id: str
    charge_id: str
    amount_cents: int
    reason: str | None = None
    reason_code: str | None = None
    created_at: datetime = field(default_factory=utc_now)
