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

PRIVATE_ROUTERS = [courses_router]


def get_private_routes_endpoints():
    endpoints = []
    for router in PRIVATE_ROUTERS:
        for route in router.routes:
            endpoints.append(route.path)  # type: ignore
    return endpoints


@app.middleware("http")
async def authenticate_routes_middleware(
    request: Request,
    call_next,
):
    if request.url.path not in get_private_routes_endpoints():
        return await call_next(request)

    API_KEY_HEADER = "Authorization"

    if not request.headers.get(API_KEY_HEADER):
        return JSONResponse(
            status_code=401,
            content={"detail": f"{API_KEY_HEADER} header is required"},
            headers={"WWW-Authenticate": "Bearer"},
        )

    token = request.headers.get(API_KEY_HEADER, "")

    SessionLocal = sessionmaker(bind=engine)
    session = SessionLocal()

    user_repository = UserRepository(User, session)

    try:
        user = auth.get_logged_user(token, user_repository)
    except HTTPException as e:
        return JSONResponse(
            status_code=e.status_code,
            content={"detail": e.detail},
            headers={"WWW-Authenticate": "Bearer"},
        )

    request.state.user = user

    session.close()
    return await call_next(request)
