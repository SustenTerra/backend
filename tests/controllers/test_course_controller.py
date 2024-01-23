import pytest

from app.controllers.course import CourseController
from app.models import Course
from app.repositories.course import CourseRepository


class TestCourseController:
    @pytest.fixture
    def setup(self, db_session, make_course, make_course_category):
        self.repository = CourseRepository(Course, db_session)
        self.controller = CourseController(Course, self.repository)

        self.created_course_category = make_course_category()
        db_session.add(self.created_course_category)
        db_session.commit()

        self.created_course: Course = make_course(
            course_category=self.created_course_category
        )
        self.repository.add(self.created_course)

    def test_list_courses(self, setup):
        couses = self.controller.get_all()

        assert couses is not None
        assert len(couses) == 1
        assert couses[0].id == self.created_course.id
        assert couses[0].name == self.created_course.name
