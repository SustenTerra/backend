from app.common.address.repository import AddressRepository
from app.common.address.schema import (
    AddressCreate,
    AddressCreateWithoutUserId,
    AddressUpdate,
)
from app.common.base.controller import BaseController
from app.common.address.exception import (
    UserAddressAlreadyRegisteredException,
    UserAddressNotFoundException,
)
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
            raise UserAddressNotFoundException()

        return address

    def update(self, user_id, update: AddressUpdate):
        found_address = self.repository.get_address_by_user_id(user_id=user_id)
        if not found_address:
            raise UserAddressNotFoundException()

        return super().update(found_address.id, update)
