from fastapi import APIRouter, Depends

from app.common.user.controller import UserController
from app.common.user.deps import get_user_controller
from app.common.user.schema import (
    UserCreate,
    UserUpdate,
    UserUpdatePassword,
    UserView,
)
from app.service import auth

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


@users.get("/users/me", tags=["users"], response_model=UserView)
def get_user(
    controller: UserController = Depends(get_user_controller),
    user: UserView = Depends(auth.get_logged_user),
):
    return controller.get_by_id(user.id)


@users.get("/users/{user_id}", tags=["users"], response_model=UserView)
def get_specific_user(
    user_id: int,
    controller: UserController = Depends(get_user_controller),
):
    return controller.get_by_id(user_id)


@users.patch("/users/me", tags=["users"], response_model=UserView)
def update_user(
    body: UserUpdate,
    controller: UserController = Depends(get_user_controller),
    user: UserView = Depends(auth.get_logged_user),
):
    return controller.update(user.id, body)


@users.patch(
    "/users/me/update_password", tags=["users"], response_model=UserView
)
def update_user_password(
    body: UserUpdatePassword,
    controller: UserController = Depends(get_user_controller),
    user: UserView = Depends(auth.get_logged_user),
):
    return controller.update_password(user.id, body)


@users.delete("/users/me", tags=["users"])
def delete_user(
    controller: UserController = Depends(get_user_controller),
    user: UserView = Depends(auth.get_logged_user),
):
    return controller.delete(user.id)
