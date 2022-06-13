from typing import List, Optional
from requests import session

from sqlmodel import Session, select

from app.lists.models import BookmarkList


def get_user_lists(db: Session, user_id: int) -> List[Optional[BookmarkList]]:
    """Return Lists of User from db by user id"""
    statement = select(BookmarkList).where(BookmarkList.user_id == user_id)
    return db.exec(statement).all()


def get_list_by_id(db: Session, id: int) -> Optional[BookmarkList]:
    """Return List from db by id"""
    statement = select(BookmarkList).where(BookmarkList.id == id)
    return db.exec(statement).first()


def create_list(db: Session, list: BookmarkList):
    """Create new list in db"""
    db.add(list)
    db.commit()


def update_list_by_id(db: Session, id: int, name: str):
    """Update list by id"""
    statement = select(BookmarkList).where(BookmarkList.id == id)
    list_to_update = db.exec(statement).first()
    list_to_update.name = name
    db.add(list_to_update)
    db.commit()
    db.refresh(list_to_update)


def delete_list_by_id(db: Session, id: int):
    """Delete list in db by id"""
    statement = select(BookmarkList).where(BookmarkList.id == id)
    list_to_delete = db.exec(statement).first()
    db.delete(list_to_delete)