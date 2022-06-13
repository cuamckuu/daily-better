
from typing import Optional

from sqlmodel import Session, select

from app.lists.models import List
from app.users.models import User
'''
[ ] GET /api/v1/users/{id}/lists - Получить публичные списки заданного пользователя
[ ] GET /api/v1/lists/{id} - Получить список по ID (имя, свойства и входящие закладки)
[ ] POST /api/v1/lists {json} - Создать новый список
[ ] PUT /api/v1/lists/{id} - Обновить существующий список
[ ] DELETE /api/v1/lists/{id} - Удалить список
'''
'''
def get_user_by_username(db: Session, username: str) -> Optional[User]:
    """Return User from db by unique username."""
    statement = select(User).where(User.username == username)
    return db.exec(statement).first()


def get_user_by_token(db: Session, token: str) -> Optional[User]:
    """Return User from db by unique token."""
    statement = select(User).where(User.token == token)
    return db.exec(statement).first()


def update_user_token(db: Session, user: User, new_token: str):
    user.token = new_token
    db.add(user)
    db.commit()
    db.refresh(user)
'''

def get_user_lists(db: Session, user: User) -> Optional[List]:
    return None