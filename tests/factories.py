import pytest

from app.models import (
    Address,
    ChapterContent,
    ContentStatusEnum,
    Course,
    CourseCategory,
    CourseChapter,
    User,
    UserContentStatus,
)


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
def make_user_teacher(faker):
    def _make_user_teacher(**kwargs):
        defaults = dict(
            email=faker.email(),
            full_name=faker.name(),
            password=faker.password(),
            phone="83940028922",
            teacher_at=faker.date_time_between(start_date="-1y", end_date="now"),
        )

        return User(**{**defaults, **kwargs})

    return _make_user_teacher


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
    def _make_course(course_category: CourseCategory, author_id=None, **kwargs):
        defaults = dict(
            name=faker.name(),
            image_key=f"{faker.text()}.png",
            author_name=faker.name(),
            description=faker.text(),
            course_category_id=course_category.id,
            author_id=author_id,
        )

        return Course(**{**defaults, **kwargs})

    return _make_course


@pytest.fixture
def make_course_published(faker):
    def _make_course(course_category: CourseCategory, author_id=None, **kwargs):
        defaults = dict(
            name=faker.name(),
            image_key=f"{faker.text()}.png",
            author_name=faker.name(),
            description=faker.text(),
            course_category_id=course_category.id,
            published_at=faker.date_time_between(start_date="-1y", end_date="now"),
            author_id=author_id,
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


@pytest.fixture
def make_user_content_status_in_progress():
    def _make_user_content_status_in_progress(
        user: User, chapter_content: ChapterContent, **kwargs
    ):
        defaults = dict(
            status=ContentStatusEnum.in_progress,
            user_id=user.id,
            chapter_content_id=chapter_content.id,
        )

        return UserContentStatus(**{**defaults, **kwargs})

    return _make_user_content_status_in_progress


@pytest.fixture
def make_user_content_status_not_started():
    def _make_user_content_status_not_started(
        user: User, chapter_content: ChapterContent, **kwargs
    ):
        defaults = dict(
            status=ContentStatusEnum.not_started,
            user_id=user.id,
            chapter_content_id=chapter_content.id,
        )

        return UserContentStatus(**{**defaults, **kwargs})

    return _make_user_content_status_not_started


@pytest.fixture
def make_chapter_content(faker):
    def _make_chapter_content(course_chapter: CourseChapter, index: int, **kwargs):
        defaults = dict(
            name=faker.name(),
            index=index,
            description=faker.text(),
            video_url=faker.image_url(),
            course_chapter_id=course_chapter.id,
        )

        return ChapterContent(**{**defaults, **kwargs})

    return _make_chapter_content


@pytest.fixture
def make_chapter_content_without_index(faker):
    def make_chapter_content_without_index(course_chapter: CourseChapter, **kwargs):
        defaults = dict(
            name=faker.name(),
            description=faker.text(),
            video_url=faker.image_url(),
            course_chapter_id=course_chapter.id,
        )

        return ChapterContent(**{**defaults, **kwargs})

    return make_chapter_content_without_index


@pytest.fixture
def make_user_address(faker):
    def _make_user_address(user_id: int, **kwargs):
        defaults = dict(
            street=faker.text(),
            number=faker.text(),
            neighborhood=faker.text(),
            complement=faker.text(),
            city=faker.text(),
            state=faker.text(),
            cep=faker.text(),
            user_id=user_id,
        )
        return Address(**{**defaults, **kwargs})

    return _make_user_address
