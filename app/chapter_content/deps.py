from fastapi import Depends
from sqlalchemy.orm import Session

from app.chapter_content.controller import ChapterContentController
from app.chapter_content.repository import ChapterContentRepository
from app.deps import get_session
from app.models import ChapterContent
from app.user.content_status import UserContentStatusRepository
from app.user.deps import get_user_content_status_repository


def get_chapter_content_repository(session: Session = Depends(get_session)):
    return ChapterContentRepository(ChapterContent, session)


def get_chapter_content_controller(
    repository: ChapterContentRepository = Depends(
        get_chapter_content_repository
    ),
    content_status_repository: UserContentStatusRepository = Depends(
        get_user_content_status_repository
    ),
):
    return ChapterContentController(
        ChapterContent, repository, content_status_repository
    )
