from fastapi import APIRouter

users = APIRouter()


@users.post("/users", tags=["users"])
def create_user():
    pass


@users.get("/users/{user_id}", tags=["users"])
def get_user(user_id: str):
    return {
        "user_id": user_id,
        "name": "John Doe",
        "age": 25,
    }


@users.get("/users", tags=["users"])
def list_users():
    pass


@users.put("/users/{user_id}", tags=["users"])
def update_user():
    pass


@users.delete("/users/{user_id}", tags=["users"])
def delete_user():
    pass
