import threading
from collections.abc import Callable
from typing import Protocol

from app.models import Charge, Refund

RefundPlan = Callable[[Charge, list[Refund]], int]
"""Decides the amount to refund from the charge and its refunds so far, or raises to reject."""


class Store(Protocol):
    """Storage interface. MemoryStore backs the unit tests, PostgresStore backs deployments."""

    def add_charge(self, charge: Charge) -> None: ...

    def get_charge(self, charge_id: str) -> Charge | None: ...

    def record_refund(
        self,
        charge_id: str,
        refund_id: str,
        plan: RefundPlan,
        reason: str | None = None,
        reason_code: str | None = None,
    ) -> Refund:
        """Atomically read the charge's refunds, run `plan`, and store the refund it returns.

        Concurrent calls for the same charge are serialized, so `plan` always sees every
        refund committed before it. An exception from `plan` stores nothing.
        """
        ...

    def list_refunds(self, charge_id: str) -> list[Refund]: ...


class MemoryStore:
    """In-memory storage. Data resets when the process restarts."""

    def __init__(self) -> None:
        self._charges: dict[str, Charge] = {}
        self._refunds: dict[str, list[Refund]] = {}
        self._lock = threading.Lock()

    def add_charge(self, charge: Charge) -> None:
        self._charges[charge.id] = charge

    def get_charge(self, charge_id: str) -> Charge | None:
        return self._charges.get(charge_id)

    def record_refund(
        self,
        charge_id: str,
        refund_id: str,
        plan: RefundPlan,
        reason: str | None = None,
        reason_code: str | None = None,
    ) -> Refund:
        with self._lock:
            charge = self._charges[charge_id]
            existing = self._refunds.setdefault(charge_id, [])
            refund = Refund(
                id=refund_id,
                charge_id=charge_id,
                amount_cents=plan(charge, list(existing)),
                reason=reason,
                reason_code=reason_code,
            )
            existing.append(refund)
            return refund

    def list_refunds(self, charge_id: str) -> list[Refund]:
        return list(self._refunds.get(charge_id, []))
