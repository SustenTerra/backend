from fastapi import APIRouter, Depends

from app.learning.chapter_content.controller import ChapterContentController
from app.learning.chapter_content.deps import get_chapter_content_controller
from app.learning.chapter_content.schema import (
    ChapterContentUpdate,
    ChapterContentView,
)
from app.models import User
from app.service.auth import get_logged_teacher_user, get_logged_user

chapter_contents = APIRouter(
    tags=["chapter_contents"],
)


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


@chapter_contents.delete(
    "/chapter_contents/{chapter_content_id}",
    description="Delete one chapter_content by id",
    response_model=None,
)
def delete_content(
    chapter_content_id: int,
    user: User = Depends(get_logged_teacher_user),
    controller: ChapterContentController = Depends(
        get_chapter_content_controller
    ),
):
    controller.delete(chapter_content_id)


@chapter_contents.patch(
    "/chapter_contents/{chapter_content_id}",
    description="Update one chapter_content by id",
    response_model=ChapterContentView,
)
def update_content(
    body: ChapterContentUpdate,
    chapter_content_id: int,
    user: User = Depends(get_logged_teacher_user),
    controller: ChapterContentController = Depends(
        get_chapter_content_controller
    ),
):
    return controller.update(chapter_content_id, body)
