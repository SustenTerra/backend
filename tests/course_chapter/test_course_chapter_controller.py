import pytest

from app.common.user.repository import UserRepository
from app.learning.chapter_content.controller import ChapterContentController
from app.learning.chapter_content.repository import ChapterContentRepository
from app.learning.course.repository import CourseRepository
from app.learning.course_category.repository import CourseCategoryRepository
from app.learning.course_chapter.controller import CourseChapterController
from app.learning.course_chapter.repository import CourseChapterRepository
from app.learning.course_chapter.schema import (
    CourseChapterCreate,
    CourseChapterUpdate,
)
from app.models import (
    ChapterContent,
    Course,
    CourseCategory,
    CourseChapter,
    User,
    UserContentStatus,
)


class TestCourseChapterController:
    @pytest.fixture
    def setup(
        self,
        db_session,
        make_user_teacher,
        make_course,
        make_course_category,
        make_course_chapter,
        make_course_chapter_with_id,
    ):
        # Create Repositories
        self.user_repository = UserRepository(User, db_session)
        self.category_repository = CourseCategoryRepository(CourseCategory, db_session)
        self.course_repository = CourseRepository(Course, db_session)
        self.repository = CourseChapterRepository(CourseChapter, db_session)
        self.chapter_content_repository = ChapterContentRepository(
            ChapterContent, db_session
        )

        # Create Controllers
        self.controller = CourseChapterController(CourseChapter, self.repository)
        self.chapter_content_controller = ChapterContentController(
            ChapterContent, self.chapter_content_repository, UserContentStatus
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

        self.session = db_session

    def test_create_course_chapter(self, setup, faker):
        # Data to be used as arguments to create a chapter
        name = faker.text()
        course_id = 1

        # Call the create of the controller to create one chapter of the course
        created_chapter = self.controller.create(
            self.created_teacher1.id,
            CourseChapterCreate(name=name, course_id=course_id),
        )
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
        updated_course_chapter = self.controller.update(
            self.created_teacher1.id, course_id, update
        )

        assert updated_course_chapter is not None
        assert updated_course_chapter.name == update.name

    def test_delete_course_chapter(
        self, setup, make_course, make_course_chapter_with_id, make_chapter_content
    ):
        other_course = make_course(self.created_category_1, self.created_teacher1.id)
        self.course_repository.add(other_course)

        new_course_chapter = make_course_chapter_with_id(
            course=other_course, index=0, id=3
        )
        self.repository.add(new_course_chapter)

        chapter_content = make_chapter_content(new_course_chapter, index=0)
        self.chapter_content_repository.add(chapter_content)

        self.controller.delete(new_course_chapter.id)

        deleted_chapter_contents = self.chapter_content_repository.get_all_chapters_contents_by_course_chapter_id(
            new_course_chapter.id
        )
        deleted_chapter = self.controller.get_by_id(new_course_chapter.id)
        course = self.course_repository.get_by_id(other_course.id)

        assert len(deleted_chapter_contents) == 0
        assert deleted_chapter is None
        assert course is not None
