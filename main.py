"""Entrypoint for backend."""

import datetime
import hashlib
import secrets
import uuid
from typing import Optional

import uvicorn
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlmodel import Session

from app.database import (User, get_db, get_user_by_token,
                          get_user_by_username, update_user_token)
from app.settings import PASSWORD_SALT

# TODO:
# - [ ] Вынести всю логику логина в отдельный blueprint
# - [ ] Сохранение токена в куки
# - [ ] Endpoint /logout
# - [ ] Регистрация
# - [ ] Тесты эндпоинтов


app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='auth')


def authenticate_user(db: Session, username: str, password: str) -> Optional[User]:
    """Return User for propper username and password pair, othervise None."""
    user = get_user_by_username(db, username)
    if not user:
        return None

    password_bytes = (password + PASSWORD_SALT).encode('utf-8')
    password_hash = hashlib.sha512(password_bytes).hexdigest()
    is_same_pass = secrets.compare_digest(password_hash, user.password_hash)
    if not is_same_pass:
        return None

    return user


@app.post('/auth')
async def login_for_access_token(
    db: Session = Depends(get_db),
    form_data: OAuth2PasswordRequestForm = Depends(),
):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Incorrect username or password',
            headers={'WWW-Authenticate': 'Bearer'},
        )

    access_token = str(uuid.uuid4())
    update_user_token(db, user, access_token)

    return {'access_token': access_token, 'token_type': 'bearer'}


def get_current_user(
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme),
):
    return get_user_by_token(db, token)


@app.get('/users/me')
async def index(user: User = Depends(get_current_user)):
    return user


if __name__ == '__main__':
    uvicorn.run(app, port=7777)
