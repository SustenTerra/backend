import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from app.models import Base
from tests.factories import *  # noqa: F401, F403


def pytest_addoption(parser):
    parser.addoption("--dburl", action="store", default="sqlite:///:memory:")


@pytest.fixture(scope="function")
def db_engine(request):
    """yields a SQLAlchemy engine which is suppressed after the test session"""
    db_url = request.config.getoption("--dburl")
    engine_ = create_engine(db_url, echo=False)

    Base.metadata.create_all(engine_)

    yield engine_

    engine_.dispose()


@pytest.fixture(scope="function")
def db_session_factory(db_engine):
    """returns a SQLAlchemy scoped session factory"""
    return scoped_session(sessionmaker(bind=db_engine))


@pytest.fixture(scope="function")
def db_session(db_session_factory):
    """yields a SQLAlchemy connection which is rollbacked after the test"""
    session_ = db_session_factory()

    yield session_

    session_.rollback()
    session_.close()


@pytest.fixture(scope="session", autouse=True)
def faker_session_locale():
    return ["pt_BR"]
