import pytest

from app.common.user.repository import UserRepository
from app.learning.course.repository import CourseRepository
from app.learning.course_category.repository import CourseCategoryRepository
from app.learning.course_chapter.repository import CourseChapterRepository
from app.models import (
    Course,
    CourseCategory,
    CourseChapter,
    User,
)


class TestCourseChapterRepository:
    @pytest.fixture
    def setup(
        self,
        db_session,
        make_user_teacher,
        make_course,
        make_course_category,
        make_course_chapter,
    ):
        # Cria os Repositórios
        self.user_repository = UserRepository(User, db_session)
        self.category_repository = CourseCategoryRepository(CourseCategory, db_session)
        self.course_repository = CourseRepository(Course, db_session)
        self.repository = CourseChapterRepository(CourseChapter, db_session)

        # Cria um usuário
        self.created_teacher: User = make_user_teacher()
        self.user_repository.add(self.created_teacher)

        # Cria as Categorias dos cursos
        self.created_category_1 = make_course_category()
        self.category_repository.add(self.created_category_1)

        # Cria um curso associado ao usuário
        self.created_course: Course = make_course(
            self.created_category_1, self.created_teacher.id
        )
        self.course_repository.add(self.created_course)

        # Cria um capítulo de curso associado ao curso
        self.created_chapter: CourseChapter = make_course_chapter(
            course=self.created_course, index=0
        )
        self.repository.add(self.created_chapter)

    def test_get_by_id(self, setup):
        found_course_chapter_by_id = self.repository.get_by_id(1)
        assert found_course_chapter_by_id is not None
        assert found_course_chapter_by_id.index == self.created_chapter.index
        assert found_course_chapter_by_id.course_id == self.created_course.id
