from datetime import datetime

from pydantic import BaseModel

from app.common.user.schema import UserView
from app.marketplace.oms.schemas.order_address import OrderAddressView
from app.marketplace.post.schema import PostView


class OrderBase(BaseModel):
    user_id: int
    post_id: int
    order_address_id: int
    total: int


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

    user: UserView
    post: PostView
    address: OrderAddressView
