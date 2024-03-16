from app.common.address.repository import AddressRepository
from app.common.address.schema import (
    AddressCreate,
    AddressCreateWithoutUserId,
    AddressUpdate,
)
from app.common.base.controller import BaseController
from app.common.user.exception import UserAddressAlreadyRegisteredException
from app.models import Address


class AddressController(
    BaseController[Address, AddressRepository, AddressCreate, AddressUpdate]
):
    def create(self, user_id: int, create: AddressCreateWithoutUserId):
        checked_address = self.repository.get_address_by_user_id(
            user_id=user_id
        )

        if checked_address:
            raise UserAddressAlreadyRegisteredException()

        address_to_create = AddressCreate(
            **create.model_dump(), user_id=user_id
        )

        return super().create(address_to_create)

    def get_address_by_user_id(self, user_id: int):
        address = self.repository.get_address_by_user_id(user_id=user_id)

        if not address:
            raise UserAddressAlreadyRegisteredException()

        return address
