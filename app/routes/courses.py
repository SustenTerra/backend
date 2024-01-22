from fastapi import APIRouter, Request

courses = APIRouter()


@courses.get(
    "/courses",
    tags=["courses"],
    description="List all courses",
)
def list_all_courses(request: Request):
    return {"full_name": request.state.user.full_name}
