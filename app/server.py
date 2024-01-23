from fastapi import FastAPI

from app.database.connection import engine
from app.models import Base
from app.routes.course_categories import (
    course_categories as course_categories_router,
)
from app.routes.courses import courses as courses_router
from app.routes.sessions import sessions as sessions_router
from app.routes.users import users as users_router

Base.metadata.create_all(engine)

app = FastAPI()

app.include_router(users_router)
app.include_router(sessions_router)
app.include_router(courses_router)
app.include_router(course_categories_router)
