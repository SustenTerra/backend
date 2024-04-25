from typing import List

from fastapi import APIRouter, Depends, Header, Request

from app.marketplace.oms.controllers.order import OrderController
from app.marketplace.oms.controllers.stripe_webhook import StripeWebhookController
from app.marketplace.oms.deps import get_order_controller, get_stripe_webhook_controller
from app.marketplace.oms.schemas.order import OMSOrderCreate, OrderView, PaymentLink
from app.models import User
from app.service.auth import get_logged_user

oms_router = APIRouter(prefix="/oms", tags=["oms"])


@oms_router.post("/payment_links", response_model=PaymentLink)
def create_payment_link(
    body: OMSOrderCreate,
    controller: OrderController = Depends(get_order_controller),
    user: User = Depends(get_logged_user),
):
    return controller.create_payment_link(user, body.post_id)


@oms_router.get("/users/me/orders", response_model=List[OrderView])
def get_orders_from_user(
    controller: OrderController = Depends(get_order_controller),
    user: User = Depends(get_logged_user),
):
    return controller.get_orders_from_user(user.id)


@oms_router.get("/sellers/me/orders", response_model=List[OrderView])
def get_orders_for_seller(
    controller: OrderController = Depends(get_order_controller),
    user: User = Depends(get_logged_user),
):
    return controller.get_orders_for_seller(user.id)


@oms_router.post("/stripe/webhook")
async def stripe_webhook(
    request: Request,
    stripe_signature: str = Header(default=None),
    controller: StripeWebhookController = Depends(get_stripe_webhook_controller),
):
    body = await request.body()
    return controller.handle_event(stripe_signature, body)
