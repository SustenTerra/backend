from fastapi import APIRouter, Depends

from app.controllers.address import AddressController
from app.deps import get_address_controller
from app.schemas.address import (
    AddressCreateWithoutUserId,
    AddressView,
)
from app.schemas.users import UserView
from app.services import auth

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
