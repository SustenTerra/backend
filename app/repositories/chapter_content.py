from app.models import ChapterContent
from app.repositories.base import BaseRepository
from app.schemas.chapter_content import ChapterContentView


class ChapterContentRepository(BaseRepository[ChapterContent]):
    def get_previous_content(
        self, content: ChapterContent
    ) -> ChapterContent | None:
        return (
            self.session.query(ChapterContent)
            .filter(
                ChapterContent.course_chapter_id == content.course_chapter_id,
                ChapterContent.index == content.index - 1,
            )
            .first()
        )

    def get_next_content(
        self, content: ChapterContent
    ) -> ChapterContent | None:
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

        previous_content = self.get_previous_content(content)
        next_content = self.get_next_content(content)

        return ChapterContentView(
            **content.__dict__,
            chapter_index=content.course_chapter.index,
            chapter_name=content.course_chapter.name,
            previous_chapter_content_id=previous_content.id
            if previous_content
            else None,
            next_chapter_content_id=next_content.id if next_content else None,
        )
