from fastapi import Depends
from sqlalchemy.orm import Session

from app.deps import get_session
from app.learning.course_chapter.controller import CourseChapterController
from app.learning.course_chapter.repository import CourseChapterRepository
from app.models import CourseChapter


def get_course_chapter_repository(session: Session = Depends(get_session)):
    return CourseChapterRepository(CourseChapter, session)


def get_course_chapter_controller(
    repository: CourseChapterRepository = Depends(get_course_chapter_repository),
):
    return CourseChapterController(CourseChapter, repository)
