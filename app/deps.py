from fastapi import Depends
from sqlalchemy.orm import Session, sessionmaker

from app.controllers.course_category import CourseCategoryController
from app.controllers.session import SessionController
from app.controllers.user import UserController
from app.database.connection import engine
from app.models import CourseCategory, User
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
