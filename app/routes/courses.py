from fastapi import APIRouter

courses = APIRouter()


@courses.get(
    "/courses",
    tags=["courses"],
    description="List all courses",
)
def list_all_courses():
    pass
