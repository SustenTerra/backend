from app.models import ContentStatusEnum, UserContentStatus
from app.base.repository import BaseRepository


class UserContentStatusRepository(BaseRepository[UserContentStatus]):
    def get_by_user_and_content(
        self, user_id: int, content_id: int
    ) -> UserContentStatus | None:
        return (
            self.session.query(UserContentStatus)
            .filter(
                UserContentStatus.user_id == user_id,
                UserContentStatus.chapter_content_id == content_id,
            )
            .first()
        )

    def get_by_user_and_content_and_status(
        self, user_id: int, content_id: int, status: ContentStatusEnum
    ) -> UserContentStatus | None:
        return (
            self.session.query(UserContentStatus)
            .filter(
                UserContentStatus.user_id == user_id,
                UserContentStatus.chapter_content_id == content_id,
                UserContentStatus.status == status,
            )
            .first()
        )
