"""Module with fastapi routes related to bookmarks."""

from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import joinedload
from sqlmodel import Session, select

from app.bookmarks.crud import (create_bookmark, delete_bookmark_with_id,
                                get_or_create_tag, update_bookmark)
from app.bookmarks.models import (Bookmark, BookmarkCreate, BookmarkDb,
                                  BookmarkUpdate,
                                  Tag,
                                  TagDb)
from app.database import get_db

router = APIRouter()


@router.post('/bookmarks')
def create_bookmark_endpoint(
    *,
    db: Session = Depends(get_db),
    bookmark: BookmarkCreate,
):
    tags = []
    for tag in bookmark.tags:
        tags.append(get_or_create_tag(db, TagDb(name=tag)))

    bookmark_db = BookmarkDb.from_orm(bookmark)
    bookmark_db.tags = tags

    create_bookmark(db, bookmark_db)


class Resp(Bookmark):
    tags: List[Tag] = []


@router.get('/bookmarks', response_model=List[Resp])
def read_bookmark_endpoint(*, db: Session = Depends(get_db)):
    res = (
        db
        .exec(select(BookmarkDb).options(joinedload(BookmarkDb.tags)))
        .unique()
        .all()
    )

    return res


@router.delete('/bookmarks/{bookmark_id}')
def delete_bookmark_endpoint(
    bookmark_id: int,
    *,
    db: Session = Depends(get_db),
):
    delete_bookmark_with_id(db, bookmark_id)


@router.patch('/bookmarks/{bookmark_id}')
def update_bookmark_endpoint(
    *,
    bookmark_id: int,
    bookmark: BookmarkUpdate,
    db: Session = Depends(get_db),
):
    update_bookmark(db, bookmark_id, bookmark)
