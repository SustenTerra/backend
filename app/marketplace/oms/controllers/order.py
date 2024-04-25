from app.common.base.controller import BaseController
from app.marketplace.oms.controllers.order_address import OrderAddressController
from app.marketplace.oms.exceptions.order import NotAvailableForOrderException
from app.marketplace.oms.repositories.order import OrderRepository
from app.marketplace.oms.schemas.order import OMSOrderCreate, OrderCreate, OrderUpdate
from app.marketplace.oms.schemas.order_address import OrderAddressCreate
from app.marketplace.post.controller import PostController
from app.marketplace.post.exception import NotFoundPostException
from app.marketplace.post.schema import PostUpdateWithImage
from app.models import Order, Post, User


class OrderController(BaseController[Order, OrderRepository, OrderCreate, OrderUpdate]):
    def __init__(
        self,
        model_class: Order,
        repository: OrderRepository,
        post_controller: PostController,
        order_address_controller: OrderAddressController,
    ):
        self.post_controller = post_controller
        self.order_address_controller = order_address_controller
        super().__init__(model_class, repository)

    def _post_order_creation_actions(self, order: Order, post: Post):
        if post.available_quantity and post.available_quantity > 0:
            # TODO: Calculate available quantity by joining with order table
            self.post_controller.update(
                post.id,
                PostUpdateWithImage(available_quantity=post.available_quantity - 1),
                order.user_id,
            )

        # TODO: Send email to user

    def create(self, user: User, body: OMSOrderCreate) -> Order:
        post = self.post_controller.get_by_id(body.post_id)
        if not post:
            raise NotFoundPostException()

        if not post.price or post.post_type != "ad":
            raise NotAvailableForOrderException()

        if post.available_quantity and post.available_quantity <= 0:
            raise NotAvailableForOrderException()

        if not user.address:
            raise NotAvailableForOrderException("User has no address.")

        order_address = self.order_address_controller.create(
            OrderAddressCreate(**user.address.__dict__)
        )

        create = OrderCreate(
            user_id=user.id,
            total=post.price,
            post_id=post.id,
            order_address_id=order_address.id,
        )

        created_order = super().create(create)
        self._post_order_creation_actions(created_order, post)

        return created_order

    def get_orders_from_user(self, user_id: int) -> list[Order]:
        return self.repository.get_orders_from_user(user_id)

    def get_orders_for_seller(self, user_id: int) -> list[Order]:
        return self.repository.get_orders_for_seller(user_id)
