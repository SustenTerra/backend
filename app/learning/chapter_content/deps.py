from fastapi import Depends
from sqlalchemy.orm import Session

from app.common.user.content_status import UserContentStatusRepository
from app.common.user.deps import get_user_content_status_repository
from app.deps import get_session
from app.learning.chapter_content.controller import ChapterContentController
from app.learning.chapter_content.repository import ChapterContentRepository
from app.models import ChapterContent


def get_chapter_content_repository(session: Session = Depends(get_session)):
    return ChapterContentRepository(ChapterContent, session)


def get_chapter_content_controller(
    repository: ChapterContentRepository = Depends(get_chapter_content_repository),
    content_status_repository: UserContentStatusRepository = Depends(
        get_user_content_status_repository
    ),
):
    return ChapterContentController(
        ChapterContent, repository, content_status_repository
    )
