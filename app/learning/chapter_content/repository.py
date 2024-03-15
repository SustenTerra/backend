from app.common.base.repository import BaseRepository
from app.learning.chapter_content.schema import ChapterContentView
from app.models import ChapterContent


class ChapterContentRepository(BaseRepository[ChapterContent]):
    def get_previous_content(self, content_id: int) -> ChapterContent | None:
        content = super().get_by_id(content_id)
        if content is None:
            return None

        return (
            self.session.query(ChapterContent)
            .filter(
                ChapterContent.course_chapter_id == content.course_chapter_id,
                ChapterContent.index == content.index - 1,
            )
            .first()
        )

    def get_next_content(self, content_id: int) -> ChapterContent | None:
        content = super().get_by_id(content_id)
        if content is None:
            return None

        return (
            self.session.query(ChapterContent)
            .filter(
                ChapterContent.course_chapter_id == content.course_chapter_id,
                ChapterContent.index == content.index + 1,
            )
            .first()
        )

    def get_by_id(self, id: int) -> ChapterContentView | None:
        content = super().get_by_id(id)

        if content is None:
            return None

        previous_content = self.get_previous_content(content.id)
        next_content = self.get_next_content(content.id)

        return ChapterContentView(
            **content.__dict__,
            chapter_index=content.course_chapter.index,
            chapter_name=content.course_chapter.name,
            previous_chapter_content_id=(
                previous_content.id if previous_content else None
            ),
            next_chapter_content_id=next_content.id if next_content else None,
        )
