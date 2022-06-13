"""Module with db operations related to bookmarks."""

from sqlmodel import Session, select

from app.bookmarks.models import BookmarkDb, TagDb


def get_or_create_tag(db: Session, tag: TagDb) -> TagDb:
    _tag = db.exec(select(TagDb).where(TagDb.name == tag.name)).first()
    if _tag:
        return _tag

    db.add(tag)
    db.commit()
    db.refresh(tag)

    return tag


def create_bookmark(db: Session, bookmark: BookmarkDb) -> BookmarkDb:
    db.add(bookmark)
    db.commit()
    db.refresh(bookmark)

    return bookmark
