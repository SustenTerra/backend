from app.schemas.users import UserView
from fastapi import APIRouter, Depends

from typing import List

from app.controllers.post import PostController
from app.deps import get_post_controller
from app.schemas.post import (
    PostCreate,
    PostView,
)
from app.services import auth

posts = APIRouter()


@posts.post(
    "/posts",
    tags=["posts"],
    response_model=PostView,
    description="Create a new post",
)
def create_post(
    body: PostCreate,
    controller: PostController = Depends(get_post_controller),
    user: UserView = Depends(auth.get_logged_user),
):
    return controller.create(body, user.id)


@posts.get(
    "/posts",
    description="List all posts",
    response_model=List[PostView],
)
def list_all_posts(
    controller: PostController = Depends(get_post_controller),
):
    return controller.get_all()


@posts.get(
    "/posts/{post_id}",
    description="Get one post by id",
    response_model=PostView,
)
def get_post_by_id(
    post_id: int,
    controller: PostController = Depends(get_post_controller),
):
    return controller.get_by_id(post_id)


# @posts.get("/posts/{post_id}", tags=["posts"], response_model=PostView)
# def get_post(
#     post_id: int,
#     controller: PostController = Depends(get_post_controller)
# ):
#     return controller.get_by_id(post_id)

# @posts.patch("/posts/me", tags=["posts"], response_model=PostView)
# def update_post(
#     body: postUpdate,
#     controller: postController = Depends(get_post_controller),
#     post: postView = Depends(auth.get_logged_post),
# ):
#     return controller.update(post.id, body)

# @posts.delete("/posts/me", tags=["posts"])
# def delete_post(
#     controller: postController = Depends(get_post_controller),
#     post: postView = Depends(auth.get_logged_post),
# ):
#     return controller.delete(post.id)
