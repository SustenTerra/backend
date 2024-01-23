from fastapi import APIRouter, Depends

from app.controllers.chapter_content import ChapterContentController
from app.deps import get_chapter_content_controller
from app.services.auth import get_logged_user

chapter_contents = APIRouter(
    tags=["chapter_contents"],
    dependencies=[Depends(get_logged_user)],
)


@chapter_contents.get(
    "/chapter_contents/{chapter_content_id}",
    description="Get one chapter_content by id",
)
def get_content_by_id(
    chapter_content_id: int,
    controller: ChapterContentController = Depends(
        get_chapter_content_controller
    ),
):
    return controller.get_by_id(chapter_content_id)
