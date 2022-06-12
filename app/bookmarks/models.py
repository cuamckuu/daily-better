"""Module to work with bookmarks related models."""

import datetime
from typing import List, Optional

from sqlmodel import (Column, DateTime, Field, Relationship, SQLModel,
                      UniqueConstraint)

UTC_TZ = datetime.timezone.utc


class BookmarkToTag(SQLModel, table=True):
    bookmark_id: int = Field(foreign_key='bookmark.id', primary_key=True)
    tag_id: int = Field(foreign_key='tag.id', primary_key=True)


class Bookmark(SQLModel, table=True):
    """Class to represent bookmark."""

    id: Optional[int] = Field(default=None, primary_key=True)
    created: datetime.datetime = Field(
        # XXX: tzinfo is ignored somewhy
        default_factory=lambda: datetime.datetime.now(tz=UTC_TZ),
        nullable=False,
        sa_column=Column(DateTime(timezone=True)),
    )
    url: str
    title: Optional[str]
    description: Optional[str]
    was_read: bool = False
    status: str = 'UNPROCESSED'

    tags: List['Tag'] = Relationship(
        back_populates='bookmarks',
        link_model=BookmarkToTag,
    )


class Tag(SQLModel, table=True):
    """Class to represent bookmark's tag."""

    __table_args__ = (UniqueConstraint('name'),)

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str

    bookmarks: List[Bookmark] = Relationship(
        back_populates='tags',
        link_model=BookmarkToTag,
    )
