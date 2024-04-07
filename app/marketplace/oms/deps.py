from fastapi import Depends
from sqlalchemy.orm import Session

from app.marketplace.oms.controllers.order import OrderController
from app.marketplace.oms.repositories.order import OrderRepository
from app.models import Order


def get_order_repository(session: Session):
    return OrderRepository(Order, session)


def get_order_controller(
    order_repository: OrderRepository = Depends(get_order_repository),
):
    return OrderController(Order, order_repository)
