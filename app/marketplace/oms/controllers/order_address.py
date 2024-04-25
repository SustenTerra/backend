from app.common.base.controller import BaseController
from app.marketplace.oms.repositories.order_address import OrderAddressRepository
from app.marketplace.oms.schemas.order_address import (
    OrderAddressCreate,
    OrderAddressUpdate,
)
from app.models import OrderAddress


class OrderAddressController(
    BaseController[
        OrderAddress, OrderAddressRepository, OrderAddressCreate, OrderAddressUpdate
    ]
):
    pass
