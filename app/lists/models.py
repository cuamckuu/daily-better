from typing import Optional

from sqlmodel import Field, Relationship, SQLModel, UniqueConstraint
from app.bookmarks.models import Bookmark

from app.users.models import User


class List(SQLModel, table=True):
    """Class to represent bookmarks lists."""

    __table_args__ = (
        UniqueConstraint('name'),
    )

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    user: Optional[User] = Relationship(back_populates="lists")
    bookmarks: Bookmark["bookmarks"] = Relationship(back_populates="list")
    

