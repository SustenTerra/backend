from app.controllers.base import BaseController
from app.models import ChapterContent
from app.repositories.chapter_content import ChapterContentRepository
from app.schemas.chapter_content import (
    ChapterContentCreate,
    ChapterContentUpdate,
)


class ChapterContentController(
    BaseController[
        ChapterContent,
        ChapterContentRepository,
        ChapterContentCreate,
        ChapterContentUpdate,
    ]
):
    pass
