from app.common.base.controller import BaseController
from app.marketplace.oms.repositories.order import OrderRepository
from app.marketplace.oms.schemas.order import OMSOrderCreate, OrderCreate, OrderUpdate
from app.models import Order, User


class OrderController(BaseController[Order, OrderRepository, OrderCreate, OrderUpdate]):
    def create(self, user: User, body: OMSOrderCreate) -> Order:
        create = OrderCreate(**body.model_dump())
        return super().create(create)
