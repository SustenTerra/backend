from fastapi import HTTPException

from app.models.user import User
from app.repositories.user import UserRepository
from app.schemas.users import UserCreate


class UserController:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    def create(self, create: UserCreate):
        found_user = self.repository.get_by_email(create.email)

        if found_user:
            raise HTTPException(
                status_code=400,
                detail="Email already registered",
            )

        user = User(
            full_name=create.full_name,
            email=create.email,
            password=create.password,
        )
        self.repository.add(user)

        return user
