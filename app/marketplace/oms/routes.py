from typing import List

from fastapi import APIRouter, Depends

from app.marketplace.oms.controllers.order import OrderController
from app.marketplace.oms.deps import get_order_controller
from app.marketplace.oms.schemas.order import OMSOrderCreate, OrderView
from app.models import User
from app.service.auth import get_logged_user

oms_router = APIRouter(prefix="/oms", tags=["oms"])


@oms_router.post("/orders", response_model=OrderView)
def create_order(
    body: OMSOrderCreate,
    controller: OrderController = Depends(get_order_controller),
    user: User = Depends(get_logged_user),
):
    return controller.create(user, body)


@oms_router.get("/users/me/orders", response_model=List[OrderView])
def get_orders_from_user(
    controller: OrderController = Depends(get_order_controller),
    user: User = Depends(get_logged_user),
):
    return controller.get_orders_from_user(user.id)


@oms_router.get("/seller/me/orders", response_model=List[OrderView])
def get_orders_for_seller(
    controller: OrderController = Depends(get_order_controller),
    user: User = Depends(get_logged_user),
):
    return controller.get_orders_for_seller(user.id)
