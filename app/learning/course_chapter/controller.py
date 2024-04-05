from app.common.base.controller import BaseController

from app.learning.course.exception import CourseIdNotFoundException
from app.learning.course.repository import CourseRepository
from app.learning.course_chapter.exception import (
    UserDontMatchCourseOwnerException,
)
from app.learning.course_chapter.repository import CourseChapterRepository
from app.learning.course_chapter.schema import (
    CourseChapterCreate,
    CourseChapterCreateWithIndex,
    CourseChapterUpdate,
)
from app.models import Course, CourseChapter


class CourseChapterController(
    BaseController[
        CourseChapter,
        CourseChapterRepository,
        CourseChapterCreateWithIndex,
        CourseChapterUpdate,
    ]
):
    def __init__(
        self,
        model_class: CourseChapter,
        repository: CourseChapterRepository,
    ):
        super().__init__(model_class, repository)
        self.course_repository = CourseRepository(Course, repository.session)

    def create(self, author_id: int, create: CourseChapterCreate):
        course = self.course_repository.get_by_id(create.course_id)
        if not course:
            raise CourseIdNotFoundException()

        if author_id != course.author_id:
            raise UserDontMatchCourseOwnerException()

        chapters = self.repository.get_all_chapters_by_course_id(course.id)

        chapter_to_create = CourseChapterCreateWithIndex(
            **create.model_dump(), index=len(chapters)
        )
        return super().create(chapter_to_create)
