"""Module to work with User related models."""
import sys
from typing import List, Optional

sys.path.append('.')
sys.path.append('..')

from sqlmodel import Field, Relationship, SQLModel, UniqueConstraint

from app.lists.models import BookmarkList


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
    lists: List[BookmarkList] = Relationship(back_populates='user')

