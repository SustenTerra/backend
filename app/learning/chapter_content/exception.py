from fastapi import HTTPException


class CannotOpenContentException(HTTPException):
    def __init__(self, chapter_content_id: int):
        super().__init__(
            status_code=400,
            detail=(
                f"Chapter content with id {chapter_content_id} "
                "cannot be seen, because it is not available yet"
            ),
        )


class ContentAlreadyExistsException(HTTPException):
    def __init__(self, chapter_content_id: int):
        super().__init__(
            status_code=400,
            detail=(
                f"Chapter content with id {chapter_content_id} "
                "already exists"
            ),
        )
