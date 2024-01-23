from typing import Optional

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
    category_name: Optional[str] = None,
    search_term: Optional[str] = None,
    controller: CourseController = Depends(get_course_controller),
):
    return controller.get_all(category_name, search_term)
