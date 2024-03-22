from typing import Optional

from app.common.base.controller import BaseController
from app.learning.chapter_content.controller import ChapterContentController
from app.learning.course.exception import NoCourseRegisteredFoundException
from app.learning.course.repository import CourseRepository
from app.learning.course.schema import (
    CourseCreate,
    CourseUpdate,
    CourseView,
    CourseCreateWithAuthorId,
)
from app.models import Course


class CourseController(
    BaseController[
        Course, CourseRepository, CourseCreateWithAuthorId, CourseUpdate
    ]
):
    def __init__(
        self,
        model_class: Course,
        repository: CourseRepository,
        content_controller: ChapterContentController,
    ):
        super().__init__(model_class, repository)
        self.content_controller = content_controller

    def create(self, user_id: int, create: CourseCreate):
        course_to_create = CourseCreateWithAuthorId(
            **create.model_dump(), author_id=user_id
        )
        return super().create(course_to_create)

    def get_all(
        self,
        category_name: Optional[str] = None,
        search_term: Optional[str] = None,
    ):
        if category_name:
            return self.repository.get_all_by_category_name(category_name)

        if search_term:
            return self.repository.get_all_by_name_or_category_name(
                search_term
            )

        return super().get_all()

    def get_by_id(self, id: int, user_id: int) -> CourseView | None:
        course = super().get_by_id(id)
        if course is None:
            return None

        course_view = CourseView.model_validate(course, from_attributes=True)

        for chapter in course_view.course_chapters:
            for content in chapter.chapter_contents:
                content.is_available = content.index == 0

                previous_content = (
                    self.content_controller.repository.get_previous_content(
                        content.id
                    )
                )

                if previous_content:
                    content.is_available = (
                        self.content_controller.content_was_viewed(
                            user_id, previous_content.id
                        )
                    )

                content.was_viewed = (
                    self.content_controller.content_was_viewed(
                        user_id, content.id
                    )
                )

        return course_view

    def get_all_in_progress(self, user_id: int):
        return self.repository.get_all_in_progress(user_id)

    def get_courses_by_teacher_id(self, user_id: int) -> list[Course]:
        courses = self.repository.get_all_by_teacher_id(user_id=user_id)

        if not courses:
            raise NoCourseRegisteredFoundException

        return courses
