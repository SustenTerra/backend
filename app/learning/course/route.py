from typing import List, Optional

from fastapi import APIRouter, Depends

from app.learning.course.controller import CourseController
from app.learning.course.deps import get_course_controller
from app.models import User
from app.learning.course.schema import CourseCreate, CourseListView, CourseView
from app.service.auth import get_logged_teacher_user, get_logged_user

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


@courses.post(
    "/courses",
    tags=["courses"],
    description="Create a course",
    response_model=CourseView,
)
def create_course(
    body: CourseCreate,
    user: User = Depends(get_logged_teacher_user),
    controller: CourseController = Depends(get_course_controller),
):
    return controller.create(user.id, body)


@courses.get(
    "/courses/in_progress",
    description="List all courses in progress",
    response_model=List[CourseListView],
)
def list_all_courses_in_progress(
    user: User = Depends(get_logged_user),
    controller: CourseController = Depends(get_course_controller),
):
    return controller.get_all_in_progress(user.id)


@courses.get(
    "/courses/{course_id}",
    description="Get one course by id",
    response_model=CourseView,
)
def get_course_by_id(
    course_id: int,
    user: User = Depends(get_logged_user),
    controller: CourseController = Depends(get_course_controller),
):
    return controller.get_by_id(course_id, user.id)
