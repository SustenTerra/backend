from fastapi import HTTPException


class UserAlreadyRegisteredException(HTTPException):
    def __init__(self, email: str):
        super().__init__(
            status_code=400,
            detail=f"Email {email} already registered",
        )


class UserPasswordDoNotMatchException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=400,
            detail="Given current password do not match actual user password",
        )


class UserNotFoundException(HTTPException):
    def __init__(self, email: str):
        super().__init__(
            status_code=404,
            detail=f"User with email {email} not found",
        )


class UserNotAllowed(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=403,
            detail="Operation forbidden for current user",
        )
