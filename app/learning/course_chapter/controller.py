from app.common.base.controller import BaseController
from app.common.user.exception import (
    CourseIdNotFoundException,
    UserDontMatchCourseOwnerException,
)
from app.learning.course.repository import CourseRepository
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

        chapters_size = self.repository.get_all_by_course_id(course.id)

        leng = len(chapters_size) - 1

        index = leng + 1

        chapter_to_create = CourseChapterCreateWithIndex(
            **create.model_dump(), index=index
        )
        return super().create(chapter_to_create)
