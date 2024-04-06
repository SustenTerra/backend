import pytest

from app.common.address.repository import AddressRepository
from app.models import Address, User
from app.common.user.repository import UserRepository
from app.common.address.schema import AddressCreateWithoutUserId, AddressUpdate
from app.common.address.controller import AddressController


class TestAddressController:
    @pytest.fixture
    def setup(
        self,
        db_session,
        make_user_address,
        make_user,
    ):
        # Create Repositories
        self.user_repository = UserRepository(User, db_session)
        self.repository = AddressRepository(Address, db_session)
        self.controller = AddressController(Address, self.repository)

        # Create users
        self.created_user1: User = make_user()
        self.created_user2: User = make_user()
        self.user_repository.add(self.created_user1)
        self.user_repository.add(self.created_user2)

        # Create Addresses
        self.user_address: Address = make_user_address(self.created_user2.id)
        self.repository.add(self.user_address)

    def test_create_address(self, setup, faker):
        create = AddressCreateWithoutUserId(
            street=faker.text(),
            number=faker.text(),
            neighborhood=faker.text(),
            complement=faker.text(),
            city=faker.text(),
            state=faker.text(),
            cep="123456789",
        )

        address = self.controller.create(self.created_user1.id, create)

        assert address is not None
        assert address.street == create.street
        assert address.number == create.number
        assert address.neighborhood == create.neighborhood
        assert address.complement == create.complement
        assert address.city == create.city
        assert address.cep == create.cep
        assert address.state == create.state
        assert address.user_id == self.created_user1.id

    def test_get_address(self, setup):
        found_address = self.repository.get_address_by_user_id(self.created_user2.id)
        assert found_address is not None
        assert found_address.street == self.user_address.street
        assert found_address.number == self.user_address.number
        assert found_address.neighborhood == self.user_address.neighborhood
        assert found_address.complement == self.user_address.complement
        assert found_address.city == self.user_address.city
        assert found_address.cep == self.user_address.cep
        assert found_address.state == self.user_address.state
        assert found_address.user_id == self.user_address.user_id

    def test_update_address(self, setup, faker):
        update = AddressUpdate(
            street=faker.text(),
            number=faker.text(),
            neighborhood=faker.text(),
            complement=faker.text(),
            city=faker.text(),
            state=faker.text(),
            cep="9876543210",
        )

        update_address = self.controller.update(self.created_user2.id, update)
        assert update_address is not None
        assert update_address.street == self.user_address.street
        assert update_address.number == self.user_address.number
        assert update_address.neighborhood == self.user_address.neighborhood
        assert update_address.complement == self.user_address.complement
        assert update_address.city == self.user_address.city
        assert update_address.cep == self.user_address.cep
        assert update_address.state == self.user_address.state
        assert update_address.user_id == self.user_address.user_id
