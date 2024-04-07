from fastapi import HTTPException


class CourseIdNotFoundException(HTTPException):
    def __init__(self):
        super().__init__(status_code=404, detail="Course ID not found")


class NoCourseRegisteredFoundException(HTTPException):
    def __init__(self):
        super().__init__(status_code=404, detail="No courses registered")
