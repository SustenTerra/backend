from fastapi import Depends
from sqlalchemy.orm import Session

from app.chapter_content.controller import ChapterContentController
from app.course.controller import CourseController
from app.course.repository import CourseRepository
from app.deps import get_chapter_content_controller, get_session
from app.models import Course


def get_course_repository(session: Session = Depends(get_session)):
    return CourseRepository(Course, session)


def get_course_controller(
    repository: CourseRepository = Depends(get_course_repository),
    content_controller: ChapterContentController = Depends(
        get_chapter_content_controller
    ),
):
    return CourseController(Course, repository, content_controller)
