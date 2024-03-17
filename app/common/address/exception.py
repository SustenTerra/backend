from fastapi import HTTPException


class UserAddressAlreadyRegisteredException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=400,
            detail="User address already registered",
        )


class UserAddressNotFoundException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=404,
            detail="User address not found",
        )
