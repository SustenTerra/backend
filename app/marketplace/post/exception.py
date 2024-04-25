from fastapi import HTTPException


class InvalidLocationException(HTTPException):
    def __init__(self, location: str):
        super().__init__(
            status_code=400,
            detail=f"State acronym {location} does not exist",
        )


class NotFoundPostException(HTTPException):
    def __init__(self):
        super().__init__(status_code=404, detail="Post not found")


class MinimumPriceRequiredException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=400, detail="Price must be greater than 50 BRL cents"
        )
