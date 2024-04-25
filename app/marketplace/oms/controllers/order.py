from app.common.base.controller import BaseController
from app.common.user.controller import UserController
from app.common.user.exception import UserIdNotFoundException
from app.marketplace.oms.controllers.order_address import OrderAddressController
from app.marketplace.oms.exceptions.order import (
    CouldNotCreatePaymentLinkException,
    NotAvailableForOrderException,
)
from app.marketplace.oms.repositories.order import OrderRepository
from app.marketplace.oms.schemas.order import (
    OrderCreate,
    OrderUpdate,
    PaymentLink,
)
from app.marketplace.oms.schemas.order_address import OrderAddressCreate
from app.marketplace.post.controller import PostController
from app.marketplace.post.exception import NotFoundPostException
from app.marketplace.post.schema import PostUpdate
from app.models import Order, Post, User
from app.service.stripe_client import StripeClient


class OrderController(BaseController[Order, OrderRepository, OrderCreate, OrderUpdate]):
    def __init__(
        self,
        model_class: Order,
        repository: OrderRepository,
        post_controller: PostController,
        user_controller: UserController,
        order_address_controller: OrderAddressController,
        stripe_client: StripeClient,
    ):
        super().__init__(model_class, repository)
        self.user_controller = user_controller
        self.post_controller = post_controller
        self.order_address_controller = order_address_controller
        self.stripe_client = stripe_client

    def _post_order_creation_actions(self, order: Order, post: Post):
        if post.available_quantity is not None and post.available_quantity > 0:
            # TODO: Calculate available quantity by joining with order table
            self.post_controller.repository.update(
                post.id,
                PostUpdate(available_quantity=post.available_quantity - 1).model_dump(
                    exclude_none=True, exclude_unset=True
                ),
            )

        # TODO: Send email to user

    def create(self, user_id: int, post_id: int) -> Order:
        user = self.user_controller.get_by_id(user_id)
        if not user:
            # TODO: send email to admin
            raise UserIdNotFoundException()

        post = self.post_controller.get_by_id(post_id)
        if not post:
            # TODO: send email to admin
            raise NotFoundPostException()

        order_address = self.order_address_controller.create(
            OrderAddressCreate(**user.address.__dict__)
        )

        create = OrderCreate(
            user_id=user.id,
            total=post.price or 0,
            post_id=post.id,
            order_address_id=order_address.id,
        )

        created_order = super().create(create)
        self._post_order_creation_actions(created_order, post)

        return created_order

    def create_payment_link(self, user: User, post_id: int) -> PaymentLink:
        post = self.post_controller.get_by_id(post_id)
        if not post:
            raise NotFoundPostException()

        if not post.price or post.post_type != "ad":
            raise NotAvailableForOrderException()

        if post.available_quantity is not None and post.available_quantity <= 0:
            raise NotAvailableForOrderException()

        if not user.address:
            raise NotAvailableForOrderException("User has no address.")

        payment_link = self.stripe_client.create_payment_link(post)
        if payment_link is None:
            raise CouldNotCreatePaymentLinkException()

        return PaymentLink(
            url=payment_link.url,
        )

    def get_orders_from_user(self, user_id: int) -> list[Order]:
        return self.repository.get_orders_from_user(user_id)

    def get_orders_for_seller(self, user_id: int) -> list[Order]:
        return self.repository.get_orders_for_seller(user_id)
