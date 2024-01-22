from fastapi import APIRouter, Depends

from app.services import auth

courses = APIRouter()

courses.dependencies = [Depends(auth.get_logged_user)]


@courses.get(
    "/courses",
    tags=["courses"],
    description="List all courses",
)
def list_all_courses():
    return {"Private routes": "Success"}
