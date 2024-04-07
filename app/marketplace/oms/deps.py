from fastapi import Depends
from sqlalchemy.orm import Session

from app.deps import get_session
from app.marketplace.oms.controllers.order import OrderController
from app.marketplace.oms.controllers.order_address import OrderAddressController
from app.marketplace.oms.repositories.order import OrderRepository
from app.marketplace.oms.repositories.order_address import OrderAddressRepository
from app.marketplace.post.controller import PostController
from app.marketplace.post.deps import get_post_controller
from app.models import Order, OrderAddress


def get_order_address_repository(session: Session = Depends(get_session)):
    return OrderAddressRepository(OrderAddress, session)


def get_order_address_controller(
    order_address_repository: OrderAddressRepository = Depends(
        get_order_address_repository
    ),
):
    return OrderAddressController(OrderAddress, order_address_repository)


def get_order_repository(session: Session = Depends(get_session)):
    return OrderRepository(Order, session)


def get_order_controller(
    order_repository: OrderRepository = Depends(get_order_repository),
    post_controller: PostController = Depends(get_post_controller),
    order_address_controller: OrderAddressController = Depends(
        get_order_address_controller
    ),
):
    return OrderController(
        Order, order_repository, post_controller, order_address_controller
    )
