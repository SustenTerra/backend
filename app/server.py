from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.chapter_content.route import (
    chapter_contents as chapter_contents_router,
)
from app.chat.route import chat as chat_router
from app.course_category.route import (
    course_categories as course_categories_router,
)
from app.course.route import courses as courses_router
from app.post_category.route import (
    post_categories as post_categories_router,
)
from app.post.route import posts as posts_router
from app.session.route import sessions as sessions_router
from app.users.route import users as users_router

app = FastAPI(title="SustenTerra")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users_router)
app.include_router(sessions_router)
app.include_router(courses_router)
app.include_router(course_categories_router)
app.include_router(post_categories_router)
app.include_router(chapter_contents_router)
app.include_router(posts_router)
app.include_router(chat_router)
