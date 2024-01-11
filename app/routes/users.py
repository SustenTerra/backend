from fastapi import APIRouter, Depends

from app.controllers.user import UserController
from app.deps import get_user_controller
from app.schemas.users import UserCreate, UserUpdate, UserView

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


@users.get("/users/{user_id}", tags=["users"], response_model=UserView)
def get_user(
    user_id: int, controller: UserController = Depends(get_user_controller)
):
    return controller.get_by_id(user_id)


@users.get("/users", tags=["users"], response_model=list[UserView])
def list_users(controller: UserController = Depends(get_user_controller)):
    return controller.get_all()


@users.patch("/users/{user_id}", tags=["users"], response_model=UserView)
def update_user(
    user_id: int,
    body: UserUpdate,
    controller: UserController = Depends(get_user_controller),
):
    return controller.update(user_id, body)


@users.delete("/users/{user_id}", tags=["users"])
def delete_user(
    user_id: int, controller: UserController = Depends(get_user_controller)
):
    return controller.delete(user_id)
