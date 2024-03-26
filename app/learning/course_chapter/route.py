from fastapi import APIRouter, Depends

from app.learning.course.schema import CourseChapterView
from app.learning.course_chapter.controller import CourseChapterController
from app.learning.course_chapter.deps import get_course_chapter_controller
from app.learning.course_chapter.schema import (
    CourseChapterCreate,
    CourseChapterUpdate,
)
from app.models import User
from app.service.auth import get_logged_teacher_user


course_chapters = APIRouter(tags=["course_chapters"])


@course_chapters.post(
    "/course_chapter",
    tags=["course_chapters"],
    description="Create course_chapter",
    response_model=CourseChapterView,
)
def create_course_chapter(
    body: CourseChapterCreate,
    user: User = Depends(get_logged_teacher_user),
    controller: CourseChapterController = Depends(
        get_course_chapter_controller
    ),
):
    return controller.create(user.id, body)


@course_chapters.patch(
    "/course_chapter/{course_chapter_id}",
    tags=["course_chapters"],
    description="Edit course_chapter",
    response_model=CourseChapterView,
)
def edit_course_chapter(
    course_chapter_id: int,
    body: CourseChapterUpdate,
    user: User = Depends(get_logged_teacher_user),
    controller: CourseChapterController = Depends(
        get_course_chapter_controller
    ),
):
    return controller.update(user.id, course_chapter_id, body)
