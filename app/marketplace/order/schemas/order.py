from pydantic import BaseModel


class OrderBase(BaseModel):
    user_id: int
    post_id: int
    order_address_id: int
