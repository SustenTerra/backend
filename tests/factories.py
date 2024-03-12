import pytest

from app.models import Course, CourseCategory, CourseChapter, User


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
            image_url=faker.image_url(),
            author_name=faker.name(),
            description=faker.text(),
            course_category_id=course_category.id,
        )

        return Course(**{**defaults, **kwargs})

    return _make_course


@pytest.fixture
def make_course_chapter(faker):
    def _make_course_chapter(course: Course, index: int, **kwargs):
        defaults = dict(
            name=faker.name(),
            index=index,
            course_id=course.id,
        )

        return CourseChapter(**{**defaults, **kwargs})

    return _make_course_chapter
