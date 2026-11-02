from fastapi import APIRouter, Depends, HTTPException

from app.deps import get_store
from app.models import Charge
from app.schemas import ChargeCreate, ChargeOut
from app.store import Store
from app.utils import is_valid_charge_amount, new_id

router = APIRouter()


@router.post("/charges", response_model=ChargeOut, status_code=201)
def create_charge(body: ChargeCreate, store: Store = Depends(get_store)) -> Charge:
    if not is_valid_charge_amount(body.amount_cents):
        raise HTTPException(400, "Charge amount is outside the allowed range")
    charge = Charge(
        id=new_id("charge"),
        amount_cents=body.amount_cents,
        currency=body.currency.lower(),
        description=body.description,
    )
    store.add_charge(charge)
    return charge


@router.get("/charges/{charge_id}", response_model=ChargeOut)
def get_charge(charge_id: str, store: Store = Depends(get_store)) -> Charge:
    charge = store.get_charge(charge_id)
    if charge is None:
        raise HTTPException(404, "Charge not found")
    return charge
