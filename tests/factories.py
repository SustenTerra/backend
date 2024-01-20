import pytest

from app.models import User


@pytest.fixture
def make_user(faker):
    def _make_user(**kwargs):
        defaults = dict(
            email=faker.email(),
            full_name=faker.name(),
            password=faker.password(),
            phone="83940028922",
        )

        return User(**{**defaults, **kwargs})

    return _make_user
