from app.common.base.repository import BaseRepository
from app.models import Order


class OrderRepository(BaseRepository[Order]):
    def get_orders_from_user(self, user_id: int) -> list[Order]:
        return self.default_query.filter(Order.user_id == user_id).all()
