import pytest

from app.models import User


@pytest.fixture
def make_user(faker):
    def _make_user(**kwargs):
        defaults = dict(
            email=faker.email(),
            full_name=faker.name(),
            password=faker.password(),
            phone=faker.phone_number(),
        )

        return User(**{**defaults, **kwargs})

    return _make_user
