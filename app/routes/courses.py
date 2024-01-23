from typing import List, Optional

from fastapi import APIRouter, Depends

from app.controllers.course import CourseController
from app.deps import get_course_controller
from app.schemas.course import CourseListView
from app.services.auth import get_logged_user

courses = APIRouter(tags=["courses"])


@courses.get(
    "/courses",
    description="List all courses",
    response_model=List[CourseListView],
)
def list_all_courses(
    category_name: Optional[str] = None,
    search_term: Optional[str] = None,
    controller: CourseController = Depends(get_course_controller),
):
    return controller.get_all(category_name, search_term)


@courses.get(
    "/courses/{course_id}",
    description="Get one course by id",
    dependencies=[Depends(get_logged_user)],
)
def get_course_by_id(
    course_id: int,
    controller: CourseController = Depends(get_course_controller),
):
    return controller.get_by_id(course_id)
