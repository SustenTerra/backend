from app.common.base.repository import BaseRepository
from app.models import Order, Post


class OrderRepository(BaseRepository[Order]):
    def get_orders_from_user(self, user_id: int) -> list[Order]:
        return self.default_query.filter(Order.user_id == user_id).all()

    def get_orders_for_seller(self, user_id: int) -> list[Order]:
        return self.default_query.filter(Order.post.has(Post.user_id == user_id)).all()
