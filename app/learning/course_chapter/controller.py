from app.common.base.controller import BaseController

from app.common.user.content_status import UserContentStatusRepository
from app.learning.chapter_content.controller import ChapterContentController
from app.learning.chapter_content.repository import ChapterContentRepository
from app.learning.course.exception import CourseIdNotFoundException
from app.learning.course.repository import CourseRepository
from app.learning.course_chapter.exception import (
    ChapterIdNotFoundException,
    UserDontMatchCourseOwnerException,
)
from app.learning.course_chapter.repository import CourseChapterRepository
from app.learning.course_chapter.schema import (
    CourseChapterCreate,
    CourseChapterCreateWithIndex,
    CourseChapterUpdate,
)
from app.models import ChapterContent, Course, CourseChapter, UserContentStatus


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
        self.course_chapter_content_repository = ChapterContentRepository(
            ChapterContent, repository.session
        )

        user_content_status_repository = UserContentStatusRepository(
            UserContentStatus, repository.session
        )

        self.chapter_content_controller = ChapterContentController(
            ChapterContent,
            self.course_chapter_content_repository,
            user_content_status_repository,
        )

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

    def update(
        self, author_id: int, course_chapter_id: int, update: CourseChapterUpdate
    ):
        chapter = self.repository.get_by_id(course_chapter_id)

        if not chapter:
            raise ChapterIdNotFoundException

        chapter_author_id = chapter.course.author_id

        if author_id != chapter_author_id:
            raise UserDontMatchCourseOwnerException()

        chapter_to_update = CourseChapterUpdate(**update.model_dump())
        return super().update(course_chapter_id, chapter_to_update)

    """def delete(self, id: int):
        #Alterar quando tiver o cascade
        course_chapter_contents = self.course_chapter_content_repository.get_all_chapters_contents_by_course_chapter_id(
            id
        )
        for chapter in course_chapter_contents:
            self.chapter_content_controller.delete(chapter.id)
        self.repository.delete(id)"""
