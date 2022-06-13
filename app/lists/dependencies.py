from fastapi import Depends
from sqlmodel import Session

import app.users.routes as routes
from app.database import get_db
from app.users.crud import get_user_by_token


def get_current_user(
    db: Session = Depends(get_db),
    token: str = Depends(routes.oauth2_scheme),
):
    """Return current user by token from header."""
    return get_user_by_token(db, token)