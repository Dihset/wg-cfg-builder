from fastapi import FastAPI

from .views import router


def create_app():
    app = FastAPI()
    app.include_router(router)
    return app
