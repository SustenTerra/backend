from app.controllers.base import BaseController
from app.exceptions.user import UserAddressAlreadyRegisteredException
from app.models import Address
from app.repositories.address import AddressRepository
from app.schemas.address import (
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
