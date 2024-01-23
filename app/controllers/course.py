from typing import Optional

from app.controllers.base import BaseController
from app.models import ContentStatusEnum, Course
from app.repositories.chapter_content import ChapterContentRepository
from app.repositories.course import CourseRepository
from app.repositories.user_content_status import UserContentStatusRepository
from app.schemas.course import CourseCreate, CourseUpdate, CourseView


class CourseController(
    BaseController[Course, CourseRepository, CourseCreate, CourseUpdate]
):
    def __init__(
        self,
        model_class: Course,
        repository: CourseRepository,
        content_repository: ChapterContentRepository,
        content_status_repository: UserContentStatusRepository,
    ):
        super().__init__(model_class, repository)
        self.content_repository = content_repository
        self.content_status_repository = content_status_repository

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

    def _content_was_viewed(self, user_id: int, content_id: int) -> bool:
        status = (
            self.content_status_repository.get_by_user_and_content_and_status(
                user_id, content_id, ContentStatusEnum.completed
            )
        )

        return status is not None

    def get_by_id(self, id: int, user_id: int) -> CourseView | None:
        course = super().get_by_id(id)
        if course is None:
            return None

        course_view = CourseView.model_validate(course, from_attributes=True)

        for chapter in course_view.course_chapters:
            for content in chapter.chapter_contents:
                content.is_available = content.index == 0

                previous_content = (
                    self.content_repository.get_previous_content(content.id)
                )

                if previous_content:
                    content.is_available = self._content_was_viewed(
                        user_id, previous_content.id
                    )

                content.was_viewed = self._content_was_viewed(
                    user_id, content.id
                )

        return course_view
