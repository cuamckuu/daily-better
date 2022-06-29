"""Entrypoint for backend."""

import uvicorn
from fastapi import FastAPI
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request

from app.bookmarks.routes import router as bookmarks_router
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
):
    context = {
        'url': url,
        'title': title,
        'request': request,
    }
    return templates.TemplateResponse('bookmarklet.html', context)


if __name__ == '__main__':
    uvicorn.run(app, port=7777)
