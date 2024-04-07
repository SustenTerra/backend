from datetime import datetime

from pydantic import BaseModel


class OrderBase(BaseModel):
    user_id: int
    post_id: int
    order_address_id: int
    value: int


class OrderCreate(OrderBase):
    pass


class OMSOrderCreate(BaseModel):
    post_id: int


class OrderUpdate(BaseModel):
    pass


class OrderView(OrderBase):
    id: int
    created_at: datetime
    updated_at: datetime
