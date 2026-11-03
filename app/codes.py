from typing import Literal

from pydantic import BaseModel

ReasonCode = Literal["duplicate", "fraudulent", "requested_by_customer", "other"]


class RefundCreate(BaseModel):
    """Optional body of POST /charges/{id}/refund."""

    reason_code: ReasonCode | None = None
