import pytest

from app.common.user.content_status import UserContentStatusRepository
from app.common.user.repository import UserRepository
from app.learning.chapter_content.controller import ChapterContentController
from app.learning.chapter_content.repository import ChapterContentRepository
from app.learning.course.repository import CourseRepository
from app.learning.course_category.repository import CourseCategoryRepository
from app.learning.course_chapter.repository import CourseChapterRepository
from app.models import (
    Course,
    CourseCategory,
    CourseChapter,
    User,
    ChapterContent,
    UserContentStatus,
)


class TestChapterContentController:
    @pytest.fixture
    def setup(
        self,
        db_session,
        make_user_teacher,
        make_course,
        make_course_category,
        make_course_chapter,
        make_chapter_content,
        make_user,
    ):
        self.user_repository = UserRepository(User, db_session)
        self.category_repository = CourseCategoryRepository(CourseCategory, db_session)
        self.course_repository = CourseRepository(Course, db_session)
        self.course_chapter_repository = CourseChapterRepository(
            CourseChapter, db_session
        )
        self.repository = ChapterContentRepository(ChapterContent, db_session)

        self.controller = ChapterContentController(
            ChapterContent,
            self.repository,
            UserContentStatusRepository(UserContentStatus, db_session),
        )

        self.created_teacher1: User = make_user_teacher()
        self.user_repository.add(self.created_teacher1)

        self.created_user: User = make_user()
        self.user_repository.add(self.created_user)

        self.created_category_1 = make_course_category()
        self.category_repository.add(self.created_category_1)

        self.created_course: Course = make_course(
            self.created_category_1, self.created_teacher1.id
        )
        self.course_repository.add(self.created_course)

        self.created_chapter: CourseChapter = make_course_chapter(
            course=self.created_course, index=0
        )
        self.course_chapter_repository.add(self.created_chapter)

        self.created_chapter_content: ChapterContent = make_chapter_content(
            course_chapter=self.created_chapter, index=2
        )
        self.repository.add(self.created_chapter_content)

    def test_create_course_chapter_content(
        self, setup, make_chapter_content_without_index
    ):
        created_chapter_content_without_index: ChapterContent = (
            make_chapter_content_without_index(course_chapter=self.created_chapter)
        )

        created_new_chapter_content = self.controller.create(
            self.created_teacher1.id, created_chapter_content_without_index
        )

        assert created_new_chapter_content is not Exception
        assert created_new_chapter_content is not None
        assert (
            created_new_chapter_content.name
            == created_chapter_content_without_index.name
        )
        assert (
            created_new_chapter_content.description
            == created_chapter_content_without_index.description
        )
        assert (
            created_new_chapter_content.video_url
            == created_chapter_content_without_index.video_url
        )

    def test_delete(self, setup):
        self.controller.delete(1)

        found_contents = self.repository.get_all()

        assert len(found_contents) == 0

    def test_update(self, setup, make_chapter_content_update):
        created_update = make_chapter_content_update()
        updated_content = self.controller.update(id=1, update=created_update)

        assert updated_content is not None
        assert created_update.name == updated_content.name
        assert created_update.description == updated_content.description
        assert created_update.video_url == updated_content.video_url

    def test_get_by_id(self, setup):
        found_content = self.controller.get_by_id(id=1, user_id=self.created_user.id)

        assert found_content is not None
        assert found_content.name == self.created_chapter_content.name
        assert found_content.description == self.created_chapter_content.description

    def test_content_was_viewed(self, setup):
        status = self.controller.content_was_viewed(
            user_id=self.created_user.id, content_id=1
        )

        assert not status

    def test_mark_content_as_viewed(self, setup):
        self.controller.mark_content_as_viewed(
            user_id=self.created_user.id, content_id=1
        )

        status = self.controller.content_was_viewed(
            user_id=self.created_user.id, content_id=1
        )

        assert status
