from fastapi import Depends
from sqlalchemy.orm import Session

from app.deps import get_session
from app.marketplace.post.controller import PostController
from app.marketplace.post.repository import PostRepository
from app.models import Post


def get_post_repository(session: Session = Depends(get_session)):
    return PostRepository(Post, session)


def get_post_controller(
    repository: PostRepository = Depends(get_post_repository),
):
    return PostController(Post, repository)
