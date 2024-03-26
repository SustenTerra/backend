import pytest

from app.common.user.repository import UserRepository
from app.learning.course.repository import CourseRepository
from app.learning.course_category.repository import CourseCategoryRepository
from app.learning.course_chapter.controller import CourseChapterController
from app.learning.course_chapter.repository import CourseChapterRepository
from app.learning.course_chapter.schema import (
    CourseChapterCreate,
    CourseChapterUpdate,
)

from app.models import Course, CourseCategory, CourseChapter, User


class TestAddressController:
    @pytest.fixture
    def setup(
        self,
        db_session,
        make_user_teacher,
        make_course,
        make_course_category,
        make_course_chapter,
    ):
        # Create Repositories
        self.user_repository = UserRepository(User, db_session)
        self.category_repository = CourseCategoryRepository(
            CourseCategory, db_session
        )
        self.course_repository = CourseRepository(Course, db_session)
        self.repository = CourseChapterRepository(CourseChapter, db_session)

        # Create Controllers
        self.controller = CourseChapterController(
            CourseChapter, self.repository
        )

        # Create User
        self.created_teacher1: User = make_user_teacher()
        self.user_repository.add(self.created_teacher1)
        self.created_teacher2: User = make_user_teacher()
        self.user_repository.add(self.created_teacher2)

        # Create Courses Categories
        self.created_category_1 = make_course_category()
        self.category_repository.add(self.created_category_1)

        # Create Courses
        self.created_course: Course = make_course(
            self.created_category_1, self.created_teacher1.id
        )
        self.course_repository.add(self.created_course)

        # Create Course Chapters
        self.created_chapter: CourseChapter = make_course_chapter(
            course=self.created_course, index=0
        )
        self.repository.add(self.created_chapter)

    def test_create_course_chapter(self, setup, faker):
        # Data to be used as arguments to create a chapter
        name = faker.text()
        course_id = 1

        # Call the create of the controller to create one chapter of the course
        created_chapter = self.controller.create(
            self.created_teacher1.id,
            CourseChapterCreate(name=name, course_id=course_id),
        )

        course = self.course_repository.get_by_id(1)
        if course:
            print(course.course_chapters)
        # Check if the course is being created
        assert created_chapter is not None

        # Check if the details are corrects
        assert created_chapter.name == name
        assert created_chapter.course_id == course_id
        assert created_chapter.index == 1

        # Create a new Chapter to check if the index is incrementing
        created_chapter2 = self.controller.create(
            self.created_teacher1.id,
            CourseChapterCreate(name=name, course_id=course_id),
        )

        assert created_chapter2 is not None

        # Check if the details are corrects
        assert created_chapter2.name == name
        assert created_chapter2.course_id == course_id
        assert created_chapter2.index == 2

    def test_update_course_chapter(self, setup):
        # Data to be used as arguments to update a chapter
        course_id = 1

        update = CourseChapterUpdate(name="new course")
        updated_course_chapter = self.controller.update(course_id, update)

        assert updated_course_chapter is not None
        assert updated_course_chapter.name == update.name
