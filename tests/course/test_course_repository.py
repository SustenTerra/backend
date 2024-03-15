import pytest

from app.common.user.repository import UserRepository
from app.learning.course.repository import CourseRepository
from app.learning.course_category.repository import CourseCategoryRepository
from app.models import (
    ChapterContent,
    Course,
    CourseCategory,
    CourseChapter,
    User,
    UserContentStatus,
)


class TestCourseRepository:
    @pytest.fixture
    def setup(self, db_session, make_course, make_course_category):
        self.repository = CourseRepository(Course, db_session)
        category_repository = CourseCategoryRepository(
            CourseCategory, db_session
        )

        self.created_category_1 = make_course_category()
        self.created_category_2 = make_course_category()
        category_repository.add(self.created_category_1)
        category_repository.add(self.created_category_2)

        self.created_course_1: Course = make_course(self.created_category_1)
        self.created_course_2: Course = make_course(self.created_category_2)
        self.repository.add(self.created_course_1)
        self.repository.add(self.created_course_2)

        self.session = db_session

    def test_get(self, setup):
        found_course = self.repository.get().first()

        assert found_course is not None
        assert found_course.id == self.created_course_1.id
        assert found_course.name == self.created_course_1.name
        assert found_course.author_name == self.created_course_1.author_name
        assert (
            found_course.course_category_id
            == self.created_course_1.course_category_id
        )

    def test_gel_all(self, setup):
        found_courses = self.repository.get_all()

        assert len(found_courses) == 2

    def test_get_all_by_category_name(self, setup):
        found_courses = self.repository.get_all_by_category_name(
            self.created_category_1.name
        )

        assert len(found_courses) == 1
        assert found_courses[0].category_name == self.created_category_1.name

    def test_get_all_by_category_name_nonexistent(self, setup):
        found_courses = self.repository.get_all_by_category_name("tint")

        assert found_courses == []

    def test_get_all_by_name_or_category_name(self, setup):
        found_courses_1 = self.repository.get_all_by_name_or_category_name(
            self.created_category_1.name
        )
        found_courses_2 = self.repository.get_all_by_name_or_category_name(
            self.created_course_2.name
        )

        assert len(found_courses_1) == 1
        assert found_courses_1[0].category_name == self.created_category_1.name

        assert len(found_courses_2) == 1
        assert found_courses_2[0].name == self.created_course_2.name

    def test_get_all_by_name_or_category_name_nonexistent(self, setup):
        found_courses = self.repository.get_all_by_name_or_category_name(
            "painting"
        )

        assert found_courses == []

    def test_get_all_in_progress_nonexistent(self, setup, make_user):
        created_user: User = make_user()
        user_repository = UserRepository(User, self.session)
        user_repository.add(created_user)
        found_user = user_repository.get_by_id(1)
        assert found_user is not None

        found_courses = self.repository.get_all_in_progress(found_user.id)

        assert found_courses == []

    def test_get_all_in_progress(
        self,
        setup,
        make_course_chapter,
        make_chapter_content,
        make_user_content_status_in_progress,
        make_user,
    ):
        created_course_chapter: CourseChapter = make_course_chapter(
            course=self.created_course_1, index=0
        )
        self.session.add(created_course_chapter)
        self.session.commit()

        created_chapter_content: ChapterContent = make_chapter_content(
            course_chapter=created_course_chapter, index=0
        )
        self.session.add(created_chapter_content)
        self.session.commit()

        created_user: User = make_user()
        user_repository = UserRepository(User, self.session)
        user_repository.add(created_user)
        found_user = user_repository.get_by_id(1)
        assert found_user is not None

        create_user_content_status: UserContentStatus = (
            make_user_content_status_in_progress(
                user=created_user, chapter_content=created_chapter_content
            )
        )
        self.session.add(create_user_content_status)
        self.session.commit()

        found_courses = self.repository.get_all_in_progress(found_user.id)

        assert len(found_courses) == 1
        assert found_courses[0].name == self.created_course_1.name

    def test_get_by_id(self, setup):
        found_course = self.repository.get_by_id(2)

        assert found_course is not None
        assert found_course.id == self.created_course_2.id
        assert found_course.name == self.created_course_2.name
        assert found_course.author_name == self.created_course_2.author_name

    def test_update(self, setup):
        new_description = "description test"
        found_course = self.repository.update(
            2, {"description": new_description}
        )

        assert found_course is not None
        assert found_course.id == self.created_course_2.id
        assert found_course.name == self.created_course_2.name
        assert found_course.author_name == self.created_course_2.author_name
        assert found_course.description == new_description

    def test_delete(self, setup):
        self.repository.delete(2)

        found_courses = self.repository.get_all()

        assert len(found_courses) == 1
