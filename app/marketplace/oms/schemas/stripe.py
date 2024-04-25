from typing import List

from pydantic import BaseModel


class CheckoutSession(BaseModel):
    id: str
    custom_fields: List[dict]
    payment_status: str
