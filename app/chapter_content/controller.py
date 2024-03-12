from app.controllers.base import BaseController
from app.chapter_content.exceptions import CannotOpenContentException
from app.models import ChapterContent, ContentStatusEnum, UserContentStatus
from app.chapter_content.repository import ChapterContentRepository
from app.users.content_status import UserContentStatusRepository
from app.chapter_content.schema import (
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
    def __init__(
        self,
        model_class: ChapterContent,
        repository: ChapterContentRepository,
        content_status_repository: UserContentStatusRepository,
    ):
        super().__init__(model_class, repository)
        self.content_status_repository = content_status_repository

    def content_was_viewed(self, user_id: int, content_id: int) -> bool:
        status = (
            self.content_status_repository.get_by_user_and_content_and_status(
                user_id, content_id, ContentStatusEnum.completed
            )
        )

        return status is not None

    def mark_content_as_viewed(self, user_id: int, content_id: int) -> None:
        if self.content_was_viewed(user_id, content_id):
            return

        self.content_status_repository.add(
            UserContentStatus(
                user_id=user_id,
                chapter_content_id=content_id,
                status=ContentStatusEnum.completed,
            )
        )

    def get_by_id(self, id: int, user_id: int) -> ChapterContent | None:
        content = super().get_by_id(id)
        if content is None:
            return None

        previous_content = self.repository.get_previous_content(content.id)
        if previous_content and not self.content_was_viewed(
            user_id, previous_content.id
        ):
            raise CannotOpenContentException(content.id)

        self.mark_content_as_viewed(
            user_id=user_id,
            content_id=content.id,
        )

        return content
