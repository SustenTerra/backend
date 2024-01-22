from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from sqlalchemy.orm import sessionmaker

from app.database.connection import engine
from app.models import Base, User
from app.repositories.user import UserRepository
from app.routes.courses import courses as courses_router
from app.routes.sessions import sessions as sessions_router
from app.routes.users import users as users_router
from app.services import auth

Base.metadata.create_all(engine)

app = FastAPI()

app.include_router(users_router)
app.include_router(sessions_router)
app.include_router(courses_router)
