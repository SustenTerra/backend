from fastapi import HTTPException

class CourseIdNotFoundException(HTTPException):
    def __init__(self):
        super().__init__(status_code=400, detail="Course ID not found")
