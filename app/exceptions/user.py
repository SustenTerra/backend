from fastapi import HTTPException


class UserAlreadyRegisteredException(HTTPException):
    def __init__(self, email: str):
        super().__init__(
            status_code=400,
            detail=f"Email {email} already registered",
        )
