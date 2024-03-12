from fastapi import Depends
from sqlalchemy.orm import Session, sessionmaker

from app.chapter_content.controller import ChapterContentController
from app.controllers.chat import ChatController
from app.controllers.course import CourseController
from app.controllers.course_category import CourseCategoryController
from app.controllers.post import PostController
from app.controllers.post_category import PostCategoryController
from app.controllers.session import SessionController
from app.users.controller import UserController
from app.database.connection import engine
from app.models import (
    ChapterContent,
    Course,
    CourseCategory,
    Post,
    PostCategory,
    User,
    UserContentStatus,
)
from app.chapter_content.repository import ChapterContentRepository
from app.repositories.course import CourseRepository
from app.repositories.course_category import CourseCategoryRepository
from app.repositories.post import PostRepository
from app.repositories.post_category import PostCategoryRepository
from app.users.repository import UserRepository
from app.users.content_status import UserContentStatusRepository
from app.services.openai_client import OpenAIClient


def get_session():
    SessionLocal = sessionmaker(bind=engine)
    session = SessionLocal()

    try:
        yield session
    finally:
        session.close()


def get_openai_client():
    return OpenAIClient()


def get_user_repository(session: Session = Depends(get_session)):
    return UserRepository(User, session)


def get_course_category_repository(session: Session = Depends(get_session)):
    return CourseCategoryRepository(CourseCategory, session)


def get_post_category_repository(session: Session = Depends(get_session)):
    return PostCategoryRepository(PostCategory, session)


def get_course_repository(session: Session = Depends(get_session)):
    return CourseRepository(Course, session)


def get_chapter_content_repository(session: Session = Depends(get_session)):
    return ChapterContentRepository(ChapterContent, session)


def get_user_content_status_repository(
    session: Session = Depends(get_session),
):
    return UserContentStatusRepository(UserContentStatus, session)


def get_post_repository(session: Session = Depends(get_session)):
    return PostRepository(Post, session)


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


def get_post_category_controller(
    repository: PostCategoryRepository = Depends(get_post_category_repository),
):
    return PostCategoryController(CourseCategory, repository)


def get_chapter_content_controller(
    repository: ChapterContentRepository = Depends(
        get_chapter_content_repository
    ),
    content_status_repository: UserContentStatusRepository = Depends(
        get_user_content_status_repository
    ),
):
    return ChapterContentController(
        ChapterContent, repository, content_status_repository
    )


def get_course_controller(
    repository: CourseRepository = Depends(get_course_repository),
    content_controller: ChapterContentController = Depends(
        get_chapter_content_controller
    ),
):
    return CourseController(Course, repository, content_controller)


def get_post_controller(
    repository: PostRepository = Depends(get_post_repository),
):
    return PostController(Post, repository)


def get_chat_controller(
    openai_client: OpenAIClient = Depends(get_openai_client),
):
    return ChatController(openai_client)
