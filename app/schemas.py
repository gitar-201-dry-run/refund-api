from datetime import datetime

from pydantic import BaseModel, Field

from app.models import ReasonCode


class ChargeCreate(BaseModel):
    amount_cents: int = Field(gt=0)
    currency: str = "usd"
    description: str = ""


class ChargeOut(BaseModel):
    id: str
    amount_cents: int
    currency: str
    description: str
    created_at: datetime


class RefundCreate(BaseModel):
    reason_code: ReasonCode | None = None


class RefundOut(BaseModel):
    id: str
    charge_id: str
    amount_cents: int
    reason: str | None
    reason_code: ReasonCode | None
    created_at: datetime
