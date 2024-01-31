from app.models import Post, PostCategory, User
from app.repositories.base import BaseRepository


class PostRepository(BaseRepository[Post]):
    def get_top_5_viewed_posts(self):
        return self.default_query.order_by(Post.views.desc()).limit(5).all()

    def get_by_search(self, search_term: str):
        return (
            self.default_query.filter(
                Post.title.ilike(f"%{search_term}%")
                | Post.location.ilike(f"%{search_term}%")
                | User.full_name.ilike(f"%{search_term}%")
                | PostCategory.name.ilike(f"%{search_term}%")
            )
            .join(Post.category)
            .join(Post.user)
            .all()
        )

    def get_by_user_id(self, user_id: int):
        return self.default_query.filter(Post.user_id == user_id).all()

    def get_by_category_name(self, category_name: str):
        return (
            self.default_query.filter(PostCategory.name == category_name)
            .join(Post.category)
            .all()
        )
