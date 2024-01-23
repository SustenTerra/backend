import pytest

from app.models import CourseCategory, User


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
