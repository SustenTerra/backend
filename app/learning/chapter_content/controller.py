from app.common.base.controller import BaseController
from app.common.user.content_status import UserContentStatusRepository
from app.learning.chapter_content.exception import (
    CannotOpenContentException,
    ContentNotFoundException,
)
from app.learning.chapter_content.repository import ChapterContentRepository
from app.learning.chapter_content.schema import (
    ChapterContentCreate,
    ChapterContentCreateWithIndex,
    ChapterContentUpdate,
)
from app.learning.course.repository import CourseRepository
from app.learning.course_chapter.exception import (
    ChapterNotFoundException,
    UserDontMatchCourseOwnerException,
)
from app.learning.course_chapter.repository import CourseChapterRepository
from app.models import (
    ChapterContent,
    ContentStatusEnum,
    Course,
    CourseChapter,
    UserContentStatus,
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
        self.course_repository = CourseRepository(Course, repository.session)
        self.chapter_repository = CourseChapterRepository(
            CourseChapter, repository.session
        )

    def create(self, author_id: int, create: ChapterContentCreate):
        course_chapter = self.chapter_repository.get_by_id(create.course_chapter_id)

        if course_chapter is None:
            raise ChapterNotFoundException()

        if author_id != course_chapter.course.author_id:
            raise UserDontMatchCourseOwnerException()

        chapter_contents = (
            self.repository.get_all_chapters_contents_by_course_chapter_id(
                course_chapter.id
            )
        )

        content_to_create = ChapterContentCreateWithIndex(
            **create.model_dump(), index=len(chapter_contents)
        )
        chapter_content = super().create(content_to_create)  # type: ignore

        return self.repository.get_by_id(chapter_content.id)

    def content_was_viewed(self, user_id: int, content_id: int) -> bool:
        status = self.content_status_repository.get_by_user_and_content_and_status(
            user_id, content_id, ContentStatusEnum.completed
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

    def update(self, id: int, update: ChapterContentUpdate) -> ChapterContent | None:
        found_content = self.repository.get_by_id(id)
        if not found_content:
            raise ContentNotFoundException()

        return super().update(id, update)
