"""Module to work with bookmarks related models."""

import datetime
from typing import List, Optional

from sqlmodel import (Column, DateTime, Field, Relationship, SQLModel,
                      UniqueConstraint)

from app.lists.models import BookmarkList

UTC_TZ = datetime.timezone.utc


class BookmarkToTag(SQLModel, table=True):
    bookmark_id: int = Field(foreign_key='bookmarkdb.id', primary_key=True)
    tag_id: int = Field(foreign_key='tagdb.id', primary_key=True)


class Bookmark(SQLModel):
    """Class to represent bookmark."""

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


class BookmarkUpdate(SQLModel):
    """Class to update bookmark."""

    url: Optional[str] = None
    title: Optional[str] = None
    description: Optional[str] = None
    was_read: Optional[bool] = None
    status: Optional[str] = None


class BookmarkDb(Bookmark, table=True):
    """Class to represent bookmark in database."""

    id: Optional[int] = Field(default=None, primary_key=True)
    list_id: Optional[int] = Field(default=None, foreign_key='bookmarklist.id')

    list: Optional[BookmarkList] = Relationship(back_populates='bookmarks')
    tags: List['TagDb'] = Relationship(
        back_populates='bookmarks',
        link_model=BookmarkToTag,
    )


class BookmarkCreate(Bookmark):
    """Class to create bookmark from fastapi endpoint."""

    tags: List[str] = []


class Tag(SQLModel):
    """Class to represent bookmark's tag."""

    name: str


class TagDb(Tag, table=True):
    """Class to represent bookmark's tag in database."""

    __table_args__ = (UniqueConstraint('name'),)

    id: Optional[int] = Field(default=None, primary_key=True)

    bookmarks: List[BookmarkDb] = Relationship(
        back_populates='tags',
        link_model=BookmarkToTag,
    )
