"""Module to work with database."""

from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool

from app.settings import DB_URL

engine = create_engine(DB_URL, connect_args={'check_same_thread': False})


def get_test_db(name=':memory:') -> Session:
    """Return test db session from sqlmodel."""
    _engine = create_engine(
        f'sqlite:///{name}',
        connect_args={'check_same_thread': False},
        poolclass=StaticPool,
    )

    SQLModel.metadata.create_all(_engine)
    with Session(_engine) as sess:
        yield sess


def get_db() -> Session:
    """Return db session from sqlmodel."""
    SQLModel.metadata.create_all(engine)
    with Session(engine) as sess:
        yield sess
