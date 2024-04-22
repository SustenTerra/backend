from typing import Annotated, List, Optional

from fastapi import APIRouter, Depends, File, Form, UploadFile

from app.learning.course.controller import CourseController
from app.learning.course.deps import get_course_controller
from app.learning.course.schema import (
    CourseCreateWithImage,
    CourseListView,
    CourseView,
)
from app.models import User
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
    image: Annotated[UploadFile, File()],
    name: Annotated[str, Form()],
    description: Annotated[str, Form()],
    course_category_id: Annotated[int, Form()],
    user: User = Depends(get_logged_teacher_user),
    controller: CourseController = Depends(get_course_controller),
):
    body = CourseCreateWithImage(
        image=image,
        name=name,
        description=description,
        course_category_id=course_category_id,
        author_name=user.full_name,
    )

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


@courses.get(
    "/users/me/courses",
    tags=["courses"],
    description="List all of the teacher's courses",
    response_model=List[CourseListView],
)
def list_all_teacher_courses(
    user: User = Depends(get_logged_teacher_user),
    controller: CourseController = Depends(get_course_controller),
):
    return controller.get_courses_by_teacher_id(user.id)


@courses.patch(
    "/users/me/courses/{course_id}/published",
    tags=["courses"],
    description="Published course",
    response_model=CourseView,
)
def publish_course(
    course_id: int,
    user: User = Depends(get_logged_teacher_user),
    controller: CourseController = Depends(get_course_controller),
):
    return controller.publish_course(course_id)


@courses.delete(
    "/courses/{course_id}",
    tags=["courses"],
    description="Delete a course by id",
    response_model=None,
)
def delete_course(
    course_id: int,
    user: User = Depends(get_logged_teacher_user),
    controller: CourseController = Depends(get_course_controller),
):
    controller.delete(course_id, user.id)
