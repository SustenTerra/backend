import pytest

from app.models import Course, CourseCategory, User


@pytest.fixture
def make_user(faker):
    def _make_user(**kwargs):
        defaults = dict(
            email=faker.email(),
            full_name=faker.name(),
            password=faker.password(),
            phone="83940028922",
        )

        return User(**{**defaults, **kwargs})

    return _make_user


@pytest.fixture
def make_course_category(faker):
    def _make_course_category(**kwargs):
        defaults = dict(
            name=faker.name(),
        )

        return CourseCategory(**{**defaults, **kwargs})

    return _make_course_category


@pytest.fixture
def make_course(faker):
    def _make_course(course_category: CourseCategory, **kwargs):
        defaults = dict(
            name=faker.name(),
            author_name=faker.name(),
            description=faker.text(),
            course_category_id=course_category.id,
        )

        return Course(**{**defaults, **kwargs})

    return _make_course
