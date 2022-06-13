"""Module to work with users database."""

from typing import Optional

from sqlmodel import Session, select

from app.users.models import User


def get_user_by_username(db: Session, username: str) -> Optional[User]:
    """Return User from db by unique username."""
    statement = select(User).where(User.username == username)
    return db.exec(statement).first()


def get_user_by_token(db: Session, token: str) -> Optional[User]:
    """Return User from db by unique token."""
    statement = select(User).where(User.token == token)
    return db.exec(statement).first()


def update_user_token(db: Session, user: User, new_token: str):
    """Update user token in db and refresh instance."""
    user.token = new_token
    db.add(user)
    db.commit()
    db.refresh(user)