from fastapi import HTTPException


class UserDontMatchCourseOwnerException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=400,
            detail="Course Author does not match the current User ",
        )
