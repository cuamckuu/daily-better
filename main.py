"""Entrypoint for backend."""

import uvicorn
from fastapi import FastAPI

from app.routes import users

app = FastAPI()

app.include_router(users.router)


if __name__ == '__main__':
    uvicorn.run(app, port=7777)
