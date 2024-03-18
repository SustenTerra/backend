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


class UserAddressAlreadyRegisteredException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=400,
            detail="User address already registered",
        )


class UserAddressNotFoundException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=400,
            detail="User address not found",
        )


class CourseIdNotFoundException(HTTPException):
    def __init__(self):
        super().__init__(status_code=400, detail="Course ID not found")


class UserDontMatchCourseOwnerException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=400,
            detail="Course Author does not match the current User ",
        )
