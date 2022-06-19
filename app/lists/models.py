from typing import List, Optional

from sqlmodel import Field, Relationship, SQLModel, UniqueConstraint


class BookmarkList(SQLModel, table=True):
    """Class to represent bookmarks lists."""

    __table_args__ = (
        UniqueConstraint('name', 'user_id'),
    )

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    user_id: Optional[int] = Field(default=None, foreign_key='user.id')

    bookmarks: List['BookmarkDb'] = Relationship(back_populates='list')
    user: Optional['User'] = Relationship(back_populates='lists')