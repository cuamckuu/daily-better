"""Entrypoint for backend."""

import uvicorn
from fastapi import Depends, FastAPI
from fastapi.requests import Request
from fastapi.templating import Jinja2Templates
from sqlmodel import Session

from app.bookmarks.crud import get_bookmark_with_url
from app.bookmarks.models import BookmarkDb
from app.bookmarks.routes import router as bookmarks_router
from app.database import get_db
from app.users.routes import router as users_router

app = FastAPI()
templates = Jinja2Templates(directory='templates')

app.include_router(users_router)
app.include_router(bookmarks_router)


@app.get('/bookmarklet')
def show_bookmarklet(
    request: Request,
    url: str,
    title: str,
    db: Session = Depends(get_db),
):
    bookmark = get_bookmark_with_url(db, url)

    context = generate_context(bookmark, url, title)
    return templates.TemplateResponse('bookmarklet.html', context)


def generate_context(bookmark: BookmarkDb, url: str, title: str):

    bookmark_exist = bookmark is not None

    context = {
            'url': bookmark.url if bookmark_exist else url,
            'title': bookmark.title if bookmark_exist else title,
            'description': bookmark.description if bookmark_exist else'',
            'wasRead': bookmark.was_read if bookmark_exist else False,
            'bookmark_id': bookmark.id if bookmark_exist else -1
        }
    return context


if __name__ == '__main__':
    uvicorn.run(app, port=7777)
