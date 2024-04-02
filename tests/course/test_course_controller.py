from unittest.mock import MagicMock

import pytest

from app.common.user.content_status import UserContentStatusRepository
from app.learning.chapter_content.controller import ChapterContentController
from app.learning.chapter_content.repository import ChapterContentRepository
from app.learning.course.controller import CourseController
from app.learning.course.repository import CourseRepository
from app.models import ChapterContent, Course, CourseChapter, UserContentStatus
from app.service.bucket_manager import BucketManager


class TestCourseController:
    @pytest.fixture
    def setup(
        self,
        db_session,
        make_course_published,
        make_course_category,
        make_course_chapter,
    ):
        bucket_manager_mock = MagicMock(spec=BucketManager)
        bucket_manager_mock.upload_file.return_value = "path/to/image.jpg"

        # Create Repositories
        self.repository = CourseRepository(Course, db_session)
        content_repository = ChapterContentRepository(
            ChapterContent, db_session
        )
        user_content_status_repository = UserContentStatusRepository(
            UserContentStatus, db_session
        )

        # Create Controllers
        chapter_content_controller = ChapterContentController(
            ChapterContent,
            content_repository,
            user_content_status_repository,
        )
        self.controller = CourseController(
            Course,
            self.repository,
            chapter_content_controller,
            bucket_manager_mock,
        )

        # Create Course Category
        self.created_course_category = make_course_category()
        db_session.add(self.created_course_category)
        db_session.commit()

        # Create Course
        self.created_course: Course = make_course_published(
            course_category=self.created_course_category
        )
        self.repository.add(self.created_course)

        # Create Course Chapter
        self.created_course_chapter: CourseChapter = make_course_chapter(
            course=self.created_course, index=0
        )
        db_session.add(self.created_course_chapter)
        db_session.commit()

        self.session = db_session

    def test_list_courses(self, setup):
        courses = self.controller.get_all()

        assert courses is not None
        assert len(courses) == 1
        assert courses[0].id == self.created_course.id
        assert courses[0].name == self.created_course.name
        assert courses[0].author_name == self.created_course.author_name
        assert courses[0].chapters_count == 1

    def test_list_courses_with_chapter(self, setup, make_course_chapter):
        created_course_chapter = make_course_chapter(
            course=self.created_course, index=1
        )
        self.session.add(created_course_chapter)
        self.session.commit()

        courses = self.controller.get_all()

        assert courses is not None
        assert len(courses) == 1
        assert courses[0].id == self.created_course.id
        assert courses[0].name == self.created_course.name
        assert courses[0].author_name == self.created_course.author_name
        assert courses[0].chapters_count == 2

    def test_list_courses_by_category_name(
        self, setup, make_course_category, make_course_published
    ):
        category_name = "TESTE"
        other_course_category = make_course_category(name=category_name)
        self.session.add(other_course_category)
        self.session.commit()

        other_course = make_course_published(
            course_category=other_course_category
        )
        self.repository.add(other_course)

        courses = self.controller.get_all(category_name=category_name)

        assert courses is not None
        assert len(courses) == 1
        assert courses[0].id != self.created_course.id
        assert courses[0].id == other_course.id

    def test_list_courses_by_search_term(
        self, setup, make_course_category, make_course_published
    ):
        search_term = "TESTE"
        search_term2 = "TESTE2"
        other_course_category = make_course_category(name=search_term)
        self.session.add(other_course_category)
        self.session.commit()

        other_course = make_course_published(
            course_category=other_course_category, name=search_term2
        )
        self.repository.add(other_course)

        courses = self.controller.get_all(search_term=search_term)

        assert courses is not None
        assert len(courses) == 1
        assert courses[0].id != self.created_course.id
        assert courses[0].id == other_course.id

        courses = self.controller.get_all(search_term=search_term2)

        assert courses is not None
        assert len(courses) == 1
        assert courses[0].id != self.created_course.id
        assert courses[0].id == other_course.id
