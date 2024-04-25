from unittest.mock import MagicMock

import pytest
from sqlalchemy.orm import Session

from app.common.user.controller import UserController
from app.common.user.repository import UserRepository
from app.marketplace.oms.controllers.order import OrderController
from app.marketplace.oms.controllers.order_address import OrderAddressController
from app.marketplace.oms.repositories.order import OrderRepository
from app.marketplace.oms.repositories.order_address import OrderAddressRepository
from app.marketplace.post.controller import PostController
from app.marketplace.post.repository import PostRepository
from app.marketplace.post.schema import PostUpdateWithImage
from app.models import Order, OrderAddress, Post, PostCategory, User
from app.service.bucket_manager import BucketManager


class TestOrderController:
    @pytest.fixture
    def setup(
        self,
        db_session: Session,
        make_user,
        make_post_category,
        make_post,
        make_user_address,
        make_stripe_client_mock,
    ):
        bucket_manager_mock = MagicMock(spec=BucketManager)
        bucket_manager_mock.upload_file.return_value = "path/to/image.jpg"
        stripe_mock = make_stripe_client_mock()

        self.user_repository = UserRepository(User, db_session)
        self.user_controller = UserController(User, self.user_repository)

        self.post_repository = PostRepository(Post, db_session)
        self.post_controller = PostController(
            Post, self.post_repository, bucket_manager_mock, stripe_mock
        )

        self.order_address_repository = OrderAddressRepository(OrderAddress, db_session)
        self.order_address_controller = OrderAddressController(
            OrderAddress, self.order_address_repository
        )

        self.order_repository = OrderRepository(Order, db_session)
        self.order_controller = OrderController(
            Order,
            self.order_repository,
            self.post_controller,
            self.user_controller,
            self.order_address_controller,
            stripe_mock,
        )

        self.seller: User = make_user()
        db_session.add(self.seller)
        db_session.commit()

        self.seller_address = make_user_address(user_id=self.seller.id)
        db_session.add(self.seller_address)
        db_session.commit()

        self.buyer: User = make_user()
        db_session.add(self.buyer)
        db_session.commit()

        self.buyer_address = make_user_address(user_id=self.buyer.id)
        db_session.add(self.buyer_address)
        db_session.commit()

        self.post_category: PostCategory = make_post_category()
        db_session.add(self.post_category)
        db_session.commit()

        self.post: Post = make_post(
            post_category=self.post_category, user=self.seller, available_quantity=10
        )
        db_session.add(self.post)
        db_session.commit()

        self.db_session = db_session

    def test_create_order(self, setup):
        assert self.post.available_quantity == 10

        order = self.order_controller.create(self.buyer.id, self.post.id)
        assert order.id is not None

        self.db_session.refresh(self.post)
        assert self.post.available_quantity == 9

    def test_availability_quantity_to_place(self, setup):
        self.post_controller.update(
            self.post.id, PostUpdateWithImage(available_quantity=0), self.seller.id
        )

        with pytest.raises(Exception) as exc_info:
            self.order_controller.create_payment_link(self.buyer, self.post.id)
        assert "Not available for order" in str(exc_info.value)

    def test_without_price_to_place(self, setup):
        self.post.price = None
        self.db_session.add(self.post)
        self.db_session.commit()

        with pytest.raises(Exception) as exc_info:
            self.order_controller.create_payment_link(self.buyer, self.post.id)
        assert "Not available for order" in str(exc_info.value)

    def test_not_found_post(self, setup):
        with pytest.raises(Exception) as exc_info:
            self.order_controller.create_payment_link(self.buyer, 999)
        assert "Post not found" in str(exc_info.value)

    def test_post_type_not_ad(self, setup):
        self.post.post_type = "other"
        self.db_session.add(self.post)
        self.db_session.commit()

        with pytest.raises(Exception) as exc_info:
            self.order_controller.create_payment_link(self.buyer, self.post.id)
        assert "Not available for order" in str(exc_info.value)

    def test_user_without_address(self, setup):
        self.db_session.delete(self.buyer_address)
        self.db_session.commit()

        with pytest.raises(Exception) as exc_info:
            self.order_controller.create_payment_link(self.buyer, self.post.id)
        assert "User has no address" in str(exc_info.value)
