from fastapi import Depends
from sqlalchemy.orm import Session

from app.deps import get_session
from app.learning.course_category.controller import CourseCategoryController
from app.learning.course_category.repository import CourseCategoryRepository
from app.models import CourseCategory


def get_course_category_repository(session: Session = Depends(get_session)):
    return CourseCategoryRepository(CourseCategory, session)


def get_course_category_controller(
    repository: CourseCategoryRepository = Depends(
        get_course_category_repository
    ),
):
    return CourseCategoryController(CourseCategory, repository)
