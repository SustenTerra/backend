from fastapi import Depends
from sqlalchemy.orm import Session

from app.address.controller import AddressController
from app.address.repository import AddressRepository
from app.deps import get_session
from app.models import Address


def get_address_repository(session: Session = Depends(get_session)):
    return AddressRepository(Address, session)


def get_address_controller(
    repository: AddressRepository = Depends(get_address_repository),
):
    return AddressController(Address, repository)
