from fastapi import APIRouter, Depends

from app.learning.chapter_content.controller import ChapterContentController
from app.learning.chapter_content.deps import get_chapter_content_controller
from app.learning.chapter_content.schema import (
    ChapterContentCreate,
    ChapterContentView,
)
from app.models import User
from app.service.auth import get_logged_teacher_user, get_logged_user

chapter_contents = APIRouter(
    tags=["chapter_contents"],
)


@chapter_contents.post(
    "/chapter_contents/",
    description="Create a chapter content",
    response_model=ChapterContentView,
)
def create(
    body: ChapterContentCreate,
    user: User = Depends(get_logged_teacher_user),
    controller: ChapterContentController = Depends(
        get_chapter_content_controller
    ),
):
    return controller.create(user.id, body)


@chapter_contents.get(
    "/chapter_contents/{chapter_content_id}",
    description="Get one chapter_content by id",
    response_model=ChapterContentView,
)
def get_content_by_id(
    chapter_content_id: int,
    user: User = Depends(get_logged_user),
    controller: ChapterContentController = Depends(
        get_chapter_content_controller
    ),
):
    return controller.get_by_id(chapter_content_id, user.id)
