"""Module to work with database."""

from typing import Optional

from sqlmodel import (Field, Session, SQLModel, UniqueConstraint,
                      create_engine, select)
from sqlmodel.pool import StaticPool

from app.settings import DB_URL

engine = create_engine(DB_URL, connect_args={'check_same_thread': False})


def get_test_db() -> Session:
    """Return test db session from sqlmodel."""
    _engine = create_engine(
        'sqlite:///:memory:',
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


class User(SQLModel, table=True):
    """Class to represent bookmarks owners."""

    __table_args__ = (
        UniqueConstraint('username'),
        UniqueConstraint('token'),
    )

    id: Optional[int] = Field(default=None, primary_key=True)
    username: str
    password_hash: str
    token: Optional[str] = None


def get_user_by_username(db: Session, username: str) -> Optional[User]:
    """Return User from db by unique username."""
    statement = select(User).where(User.username == username)
    return db.exec(statement).first()


def get_user_by_token(db: Session, token: str) -> Optional[User]:
    """Return User from db by unique token."""
    statement = select(User).where(User.token == token)
    return db.exec(statement).first()


def update_user_token(db: Session, user: User, new_token: str):
    user.token = new_token
    db.add(user)
    db.commit()
    db.refresh(user)
