from typing import Optional

from pydantic import BaseModel, Field


class CheckoutMetadata(BaseModel):
    post_id: Optional[str] = Field(default=None)
    user_id: Optional[str] = Field(default=None)


class CheckoutSession(BaseModel):
    id: str
    metadata: Optional[CheckoutMetadata] = Field(default=None)
    payment_status: str
