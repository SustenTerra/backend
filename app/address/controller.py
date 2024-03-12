from app.base.controller import BaseController
from app.user.exception import UserAddressAlreadyRegisteredException
from app.models import Address
from app.address.repository import AddressRepository
from app.address.schema import (
    AddressCreate,
    AddressCreateWithoutUserId,
    AddressUpdate,
)


class AddressController(
    BaseController[Address, AddressRepository, AddressCreate, AddressUpdate]
):
    def create(self, user_id, create: AddressCreateWithoutUserId):
        found_user_id = self.repository.get_address_by_user_id(user_id=user_id)

        if found_user_id:
            raise UserAddressAlreadyRegisteredException()

        address_to_create = AddressCreate(
            **create.model_dump(), user_id=user_id
        )

        return super().create(address_to_create)
