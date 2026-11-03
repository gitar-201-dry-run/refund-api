from pydantic import BaseModel


class RefundCreate(BaseModel):
    """Optional body of POST /charges/{id}/refund."""

    reason_code: str | None = None
