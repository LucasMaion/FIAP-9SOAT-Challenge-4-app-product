from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class PaymentMetadataEntity(BaseModel):
    id: int = Field(..., gt=0)
    created_at: datetime
    updated_at: datetime
    deleted_at: Optional[datetime] = None
    payment_id: str
    provider_transaction_id: str
