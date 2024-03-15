from fastapi import Depends
from sqlalchemy.orm import Session

from app.deps import get_session
from app.marketplace.post_category.controller import PostCategoryController
from app.marketplace.post_category.repository import PostCategoryRepository
from app.models import PostCategory


def get_post_category_repository(session: Session = Depends(get_session)):
    return PostCategoryRepository(PostCategory, session)


def get_post_category_controller(
    repository: PostCategoryRepository = Depends(get_post_category_repository),
):
    return PostCategoryController(PostCategory, repository)
