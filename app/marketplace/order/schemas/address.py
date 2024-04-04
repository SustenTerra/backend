from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class OrderAddressBase(BaseModel):
    street: str
    number: str
    neighborhood: str
    complement: Optional[str]
    city: str
    state: str
    cep: str


class OrderAddressCreate(OrderAddressBase):
    pass


class OrderAddressUpdate(BaseModel):
    street: Optional[str]
    number: Optional[str]
    neighborhood: Optional[str]
    complement: Optional[str]
    city: Optional[str]
    state: Optional[str]
    cep: Optional[str]


class OrderAddressView(OrderAddressBase):
    id: int
    created_at: datetime
    updated_at: datetime
