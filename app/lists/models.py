import sys
from typing import Optional

from sqlmodel import Field, Relationship, SQLModel, UniqueConstraint

sys.path.append('.')
sys.path.append('..')


class BookmarkList(SQLModel, table=True):
    """Class to represent bookmarks lists."""

    __table_args__ = (
        UniqueConstraint('name'),
    )

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    user_id: Optional[int] = Field(default=None, foreign_key="user.id")
    user: Optional["User"] = Relationship(back_populates="lists")
    

