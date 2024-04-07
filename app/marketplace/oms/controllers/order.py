from app.common.base.controller import BaseController
from app.marketplace.oms.repositories.order import OrderRepository
from app.marketplace.oms.schemas.order import OrderCreate, OrderUpdate
from app.models import Order


class OrderController(BaseController[Order, OrderRepository, OrderCreate, OrderUpdate]):
    pass
