import pytest

from app.common.user.content_status import UserContentStatusRepository
from app.common.user.repository import UserRepository
from app.learning.chapter_content.controller import ChapterContentController
from app.learning.chapter_content.repository import ChapterContentRepository
from app.learning.course.repository import CourseRepository
from app.learning.course_category.repository import CourseCategoryRepository
from app.learning.course_chapter.repository import CourseChapterRepository
from app.learning.chapter_content.schema import ChapterContentCreate
from app.models import (
    Course,
    CourseCategory,
    CourseChapter,
    User,
    ChapterContent,
    UserContentStatus,
)


class TestCourseChapterContentController:
    @pytest.fixture
    def setup(
        self,
        db_session,
        make_user_teacher,
        make_course,
        make_course_category,
        make_course_chapter,
        make_chapter_content_without_index,
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

        self.created_chapter_content: ChapterContent = (
            make_chapter_content_without_index(course_chapter=self.created_chapter)
        )

    def test_create_course_chapter_content(self, setup, faker):
        name = faker.text()
        description = faker.text()
        video_url = faker.text()
        course_chapter_id = self.created_chapter.id

        body = ChapterContentCreate(
            name=name,
            description=description,
            video_url=video_url,
            course_chapter_id=course_chapter_id,
        )
        created__new_chapter_content = self.controller.create(
            self.created_teacher1.id, body
        )

        assert created__new_chapter_content is not Exception
        assert created__new_chapter_content is not None
        assert created__new_chapter_content.name == body.name
        assert created__new_chapter_content.description == body.description
        assert created__new_chapter_content.video_url == body.video_url
