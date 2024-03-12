from fastapi import Depends
from sqlalchemy.orm import Session, sessionmaker

from app.chapter_content.controller import ChapterContentController
from app.chat.controller import ChatController
from app.course.controller import CourseController
from app.course_category.controller import CourseCategoryController
from app.post.controller import PostController
from app.post_category.controller import PostCategoryController
from app.session.controller import SessionController
from app.user.controller import UserController
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
from app.course.repository import CourseRepository
from app.course_category.repository import CourseCategoryRepository
from app.post.repository import PostRepository
from app.post_category.repository import PostCategoryRepository
from app.user.repository import UserRepository
from app.user.content_status import UserContentStatusRepository
from app.service.openai_client import OpenAIClient


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
