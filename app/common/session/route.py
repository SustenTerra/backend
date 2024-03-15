from fastapi import APIRouter, Depends

from app.common.session.controller import SessionController
from app.common.session.deps import get_session_controller
from app.common.session.schema import LoginPayload, LoginView

sessions = APIRouter()


@sessions.post(
    "/sessions",
    tags=["sessions"],
    response_model=LoginView,
    description="Return JWT Token and User information",
)
def make_login(
    body: LoginPayload,
    controller: SessionController = Depends(get_session_controller),
):
    return controller.login(body.email, body.password)
