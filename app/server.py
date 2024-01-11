from fastapi import FastAPI

from app.database.connection import engine
from app.models import Base
from app.routes.users import users as users_router

Base.metadata.create_all(engine)

app = FastAPI()

app.include_router(users_router)
