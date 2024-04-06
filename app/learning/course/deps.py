from fastapi import Depends
from sqlalchemy.orm import Session

from app.deps import get_bucket_manager, get_session
from app.learning.chapter_content.controller import ChapterContentController
from app.learning.chapter_content.deps import get_chapter_content_controller
from app.learning.course.controller import CourseController
from app.learning.course.repository import CourseRepository
from app.models import Course
from app.service.bucket_manager import BucketManager


def get_course_repository(session: Session = Depends(get_session)):
    return CourseRepository(Course, session)


def get_course_controller(
    repository: CourseRepository = Depends(get_course_repository),
    content_controller: ChapterContentController = Depends(
        get_chapter_content_controller
    ),
    bucket_manager: BucketManager = Depends(get_bucket_manager),
):
    return CourseController(Course, repository, content_controller, bucket_manager)
