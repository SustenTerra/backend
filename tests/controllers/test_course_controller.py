import pytest

from app.controllers.course import CourseController
from app.models import Course
from app.repositories.course import CourseRepository


class TestCourseController:
    @pytest.fixture
    def setup(self, db_session, make_course, make_course_category):
        self.session = db_session
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
        courses = self.controller.get_all()

        assert courses is not None
        assert len(courses) == 1
        assert courses[0].id == self.created_course.id
        assert courses[0].name == self.created_course.name

    def test_list_courses_by_category_name(
        self, setup, make_course_category, make_course
    ):
        category_name = "TESTE"
        other_course_category = make_course_category(name=category_name)
        self.session.add(other_course_category)
        self.session.commit()

        other_course = make_course(course_category=other_course_category)
        self.repository.add(other_course)

        courses = self.controller.get_all(category_name=category_name)

        assert courses is not None
        assert len(courses) == 1
        assert courses[0].id != self.created_course.id
        assert courses[0].id == other_course.id

    def test_list_courses_by_search_term(
        self, setup, make_course_category, make_course
    ):
        search_term = "TESTE"
        search_term2 = "TESTE2"
        other_course_category = make_course_category(name=search_term)
        self.session.add(other_course_category)
        self.session.commit()

        other_course = make_course(
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
