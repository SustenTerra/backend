from fastapi import APIRouter, Depends

from app.chapter_content.controller import ChapterContentController
from app.chapter_content.deps import get_chapter_content_controller
from app.chapter_content.schema import ChapterContentView
from app.models import User
from app.service.auth import get_logged_user

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
