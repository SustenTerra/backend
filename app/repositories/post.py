from app.models import Post
from app.repositories.base import BaseRepository


class PostRepository(BaseRepository[Post]):
    def get_top_5_viewed_posts(self):
        return self.default_query.order_by(Post.views.desc()).limit(5).all()
