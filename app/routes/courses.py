from fastapi import APIRouter, Depends

from app.controllers.course import CourseController
from app.deps import get_course_controller

courses = APIRouter()


@courses.get(
    "/courses",
    tags=["courses"],
    description="List all courses",
)
def list_all_courses(
    controller: CourseController = Depends(get_course_controller),
):
    return controller.get_all()
