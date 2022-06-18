"""Entrypoint for backend."""

import uvicorn
from fastapi import FastAPI

from app.bookmarks.routes import router as bookmarks_router
from app.users.routes import router as users_router

app = FastAPI()

app.include_router(users_router)
app.include_router(bookmarks_router)


if __name__ == '__main__':
    uvicorn.run(app, port=7777)
