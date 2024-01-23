import pytest

from app.controllers.course_category import CourseCategoryController
from app.models import CourseCategory
from app.repositories.course_category import CourseCategoryRepository


class TestCourseCategoryController:
    @pytest.fixture
    def setup(self, db_session, make_course_category):
        self.repository = CourseCategoryRepository(CourseCategory, db_session)
        self.controller = CourseCategoryController(
            CourseCategory, self.repository
        )

        self.created_category: CourseCategory = make_course_category()
        self.repository.add(self.created_category)

    def test_list_categories(self, setup):
        categories = self.controller.get_all()

        assert categories is not None
        assert len(categories) == 1
        assert categories[0].id == self.created_category.id
        assert categories[0].name == self.created_category.name
