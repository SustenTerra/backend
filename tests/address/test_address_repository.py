import pytest

from app.common.address.repository import AddressRepository
from app.models import Address
from app.common.user.repository import UserRepository
from app.models import User


class TestAddressRepository:
    @pytest.fixture
    def setup(self, db_session, make_user_address, make_user):
        # Cria os repositórios
        self.user_repository = UserRepository(User, db_session)
        self.repository = AddressRepository(Address, db_session)

        # Cria um usuário
        self.created_user1: User = make_user()
        self.user_repository.add(self.created_user1)

        # Cria um endereço
        self.user_address: Address = make_user_address(self.created_user1.id)
        self.repository.add(self.user_address)

    def test_get(self, setup):
        found_address = self.repository.get().first()

        assert found_address is not None
        assert found_address.street == self.user_address.street
        assert found_address.number == self.user_address.number
        assert found_address.neighborhood == self.user_address.neighborhood
        assert found_address.complement == self.user_address.complement
        assert found_address.city == self.user_address.city
        assert found_address.state == self.user_address.state
        assert found_address.cep == self.user_address.cep

    def test_get_all(self, setup):
        found_addresses = self.repository.get_all()

        assert len(found_addresses) == 1

    def test_get_by_id(self, setup):
        found_user_by_id = self.repository.get_by_id(1)

        assert found_user_by_id is not None
        assert found_user_by_id.street == self.user_address.street
        assert found_user_by_id.number == self.user_address.number
        assert found_user_by_id.neighborhood == self.user_address.neighborhood
        assert found_user_by_id.complement == self.user_address.complement
        assert found_user_by_id.city == self.user_address.city
        assert found_user_by_id.state == self.user_address.state
        assert found_user_by_id.cep == self.user_address.cep

    def get_address_by_user_id(self, setup):
        found_user_address = self.repository.get_by_id(id=1)

        assert found_user_address is not None
        assert found_user_address.id == self.created_user1.id
