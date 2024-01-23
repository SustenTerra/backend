from app.controllers.base import BaseController
from app.models import Course
from app.repositories.course import CourseRepository
from app.schemas.course import CourseCreate, CourseUpdate


class CourseController(
    BaseController[Course, CourseRepository, CourseCreate, CourseUpdate]
):
    pass
