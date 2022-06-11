"""Module to work with database."""

from typing import Optional

from sqlmodel import Field, Session, SQLModel, UniqueConstraint, create_engine, select

from app.settings import DB_URL

engine = create_engine(DB_URL)


def get_db(is_test=False) -> Session:
    """Return db session from sqlmodel."""
    _engine = engine
    if is_test:
        _engine = create_engine('sqlite:///:memory:')

    SQLModel.metadata.create_all(_engine)
    with Session(_engine) as sess:
        yield sess


class User(SQLModel, table=True):
    """Class to represent bookmarks owners."""

    __table_args__ = (UniqueConstraint('username'),)

    id: Optional[int] = Field(default=None, primary_key=True)
    username: str
    password_hash: str
    token: Optional[str] = None


def get_user_by_username(db: Session, username: str) -> Optional[User]:
    """Return User from db by unique username."""
    statement = select(User).where(User.username == username)
    return db.exec(statement).first()
