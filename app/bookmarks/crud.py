"""Module with db operations related to bookmarks."""

from fastapi import HTTPException
from sqlmodel import Session, select

from app.bookmarks.models import BookmarkDb, BookmarkUpdate, TagDb


def get_or_create_tag(db: Session, tag: TagDb) -> TagDb:
    _tag = db.exec(select(TagDb).where(TagDb.name == tag.name)).first()
    if _tag:
        return _tag

    db.add(tag)
    db.commit()
    db.refresh(tag)

    return tag


def get_bookmark_with_url(db: Session, url: str) -> BookmarkDb:
    bookmark = db.exec(select(BookmarkDb).where(BookmarkDb.url == url)).first()

    return bookmark


def get_bookmark_with_id(db: Session, id: int) -> BookmarkDb:
    bookmark = db.exec(select(BookmarkDb).where(BookmarkDb.id == id)).first()

    return bookmark


def delete_bookmark_with_id(db: Session, id: int):
    bookmark = get_bookmark_with_id(db, id)
    db.delete(bookmark)
    db.commit()


def create_bookmark(db: Session, bookmark: BookmarkDb) -> BookmarkDb:
    db.add(bookmark)
    db.commit()
    db.refresh(bookmark)

    return bookmark


def update_bookmark(db: Session, id: int, new_bookmark: BookmarkUpdate):
    bookmark = get_bookmark_with_id(db, id)

    if not bookmark:
        raise HTTPException(status_code=404, detail="Bookmark not found")
    bookmark_data = new_bookmark.dict(exclude_unset=True)
    for key, value in bookmark_data.items():
        if value:
            setattr(bookmark, key, value)
    db.add(bookmark)
    db.commit()
