from fastapi import APIRouter, Depends

from app.controllers.user import UserController
from app.deps import get_user_controller
from app.schemas.users import UserCreate, UserView

users = APIRouter()


@users.post(
    "/users",
    tags=["users"],
    response_model=UserView,
    description="Create a new user",
)
def create_user(
    body: UserCreate, controller: UserController = Depends(get_user_controller)
):
    return controller.create(body)


@users.get("/users/{user_id}", tags=["users"])
def get_user(user_id: str):
    return {
        "user_id": user_id,
        "name": "John Doe",
        "age": 25,
    }


@users.get("/users", tags=["users"])
def list_users():
    pass


@users.patch("/users/{user_id}", tags=["users"])
def update_user():
    pass


@users.delete("/users/{user_id}", tags=["users"])
def delete_user():
    pass
