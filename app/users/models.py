from typing import Optional

from sqlmodel import Field, SQLModel, UniqueConstraint


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

