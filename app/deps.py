from fastapi import Depends
from sqlalchemy.orm import Session, sessionmaker

from app.controllers.chapter_content import ChapterContentController
from app.controllers.course import CourseController
from app.controllers.course_category import CourseCategoryController
from app.controllers.session import SessionController
from app.controllers.user import UserController
from app.database.connection import engine
from app.models import ChapterContent, Course, CourseCategory, User
from app.repositories.chapter_content import ChapterContentRepository
from app.repositories.course import CourseRepository
from app.repositories.course_category import CourseCategoryRepository
from app.repositories.user import UserRepository


def get_session():
    SessionLocal = sessionmaker(bind=engine)
    session = SessionLocal()

    try:
        yield session
    finally:
        session.close()


def get_user_repository(session: Session = Depends(get_session)):
    return UserRepository(User, session)


def get_course_category_repository(session: Session = Depends(get_session)):
    return CourseCategoryRepository(CourseCategory, session)


def get_course_repository(session: Session = Depends(get_session)):
    return CourseRepository(Course, session)


def get_chapter_content_repository(session: Session = Depends(get_session)):
    return ChapterContentRepository(ChapterContent, session)


def get_user_controller(
    repository: UserRepository = Depends(get_user_repository),
):
    return UserController(User, repository)


def get_session_controller(
    user_repository: UserRepository = Depends(get_user_repository),
):
    return SessionController(user_repository)


def get_course_category_controller(
    repository: CourseCategoryRepository = Depends(
        get_course_category_repository
    ),
):
    return CourseCategoryController(CourseCategory, repository)


def get_course_controller(
    repository: CourseRepository = Depends(get_course_repository),
):
    return CourseController(Course, repository)


def get_chapter_content_controller(
    repository: ChapterContentRepository = Depends(
        get_chapter_content_repository
    ),
):
    return ChapterContentController(ChapterContent, repository)
