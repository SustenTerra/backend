from fastapi import FastAPI

from app.database.connection import engine
from app.models import Base
from app.routes.chapter_contents import (
    chapter_contents as chapter_contents_router,
)
from app.routes.course_categories import (
    course_categories as course_categories_router,
)
from app.routes.courses import courses as courses_router
from app.routes.post_categories import (
    post_categories as post_categories_router,
)
from app.routes.posts import posts as posts_router
from app.routes.sessions import sessions as sessions_router
from app.routes.users import users as users_router

Base.metadata.create_all(engine)

app = FastAPI()

app.include_router(users_router)
app.include_router(sessions_router)
app.include_router(courses_router)
app.include_router(course_categories_router)
app.include_router(post_categories_router)
app.include_router(chapter_contents_router)
app.include_router(posts_router)
