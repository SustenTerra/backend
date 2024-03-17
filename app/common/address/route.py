from fastapi import APIRouter, Depends

from app.common.address.controller import AddressController
from app.common.address.deps import get_address_controller
from app.common.address.schema import (
    AddressCreateWithoutUserId,
    AddressUpdate,
    AddressView,
)
from app.common.user.schema import UserView
from app.service import auth

addresses = APIRouter(
    dependencies=[
        Depends(auth.get_logged_user),
    ]
)


@addresses.post(
    "/users/me/addresses",
    tags=["addresses"],
    response_model=AddressView,
    description="Create a new Address for user",
)
def create_user_address(
    body: AddressCreateWithoutUserId,
    controller: AddressController = Depends(get_address_controller),
    user: UserView = Depends(auth.get_logged_user),
):
    return controller.create(user.id, body)


@addresses.get(
    "/users/me/addresses",
    tags=["addresses"],
    response_model=AddressView,
    description="Get Users Addresses",
)
def get_address(
    controller: AddressController = Depends(get_address_controller),
    user: UserView = Depends(auth.get_logged_user),
):
    return controller.get_address_by_user_id(user.id)


@addresses.patch(
    "/users/me/addresses",
    tags=["addresses"],
    response_model=AddressView,
    description="Update User Address",
)
def update_address(
    body: AddressUpdate,
    controller: AddressController = Depends(get_address_controller),
    user: UserView = Depends(auth.get_logged_user),
):
    return controller.update(user.id, body)
