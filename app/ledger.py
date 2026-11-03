from app.models import Refund
from app.store import RefundPlan, Store
from app.utils import new_id


def record_refund(
    store: Store,
    charge_id: str,
    plan: RefundPlan,
    reason: str | None = None,
    reason_code: str | None = None,
) -> Refund:
    """Write a refund to the ledger for a charge and return it.

    The store runs `plan` while it holds the charge, so the amount it returns is decided
    against the refunds that exist at the moment of the write.
    """
    return store.record_refund(charge_id, new_id("refund"), plan, reason=reason, reason_code=reason_code)
