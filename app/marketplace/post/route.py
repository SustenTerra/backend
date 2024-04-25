from typing import Annotated, List, Optional

from fastapi import APIRouter, Depends, File, Form, UploadFile

from app.common.user.schema import UserView
from app.marketplace.post.controller import PostController
from app.marketplace.post.deps import get_post_controller
from app.marketplace.post.schema import (
    PostCreateWithImage,
    PostUpdateWithImage,
    PostView,
)
from app.service import auth

posts = APIRouter()


@posts.post(
    "/posts",
    tags=["posts"],
    response_model=PostView,
    description="Create a new post",
)
def create_post(
    image: Annotated[UploadFile, File()],
    title: Annotated[str, Form()],
    description: Annotated[str, Form()],
    price: Annotated[Optional[int], Form()],
    post_type: Annotated[str, Form()],
    location: Annotated[str, Form()],
    category_id: Annotated[int, Form()],
    available_quantity: Optional[int] = Form(default=None),
    controller: PostController = Depends(get_post_controller),
    user: UserView = Depends(auth.get_logged_user),
):
    body = PostCreateWithImage(
        title=title,
        image=image,
        description=description,
        price=price,
        post_type=post_type,
        available_quantity=available_quantity,
        location=location,
        category_id=category_id,
        user_id=user.id,
    )

    return controller.create(body)


@posts.get(
    "/posts",
    tags=["posts"],
    description="List all posts",
    response_model=List[PostView],
)
def list_all_posts(
    search_term: Optional[str] = None,
    user_id: Optional[int] = None,
    category_name: Optional[str] = None,
    location: Optional[str] = None,
    controller: PostController = Depends(get_post_controller),
):
    return controller.get_all(search_term, user_id, category_name, location)


@posts.get(
    "/posts/{post_id}",
    tags=["posts"],
    description="Get one post by id",
    response_model=PostView,
)
def get_post_by_id(
    post_id: int,
    controller: PostController = Depends(get_post_controller),
):
    return controller.get_by_id(post_id)


@posts.patch("/posts/{post_id}", tags=["posts"], response_model=PostView)
def update_post(
    post_id: int,
    image: Optional[UploadFile] = File(default=None),
    title: Optional[str] = Form(default=None),
    description: Optional[str] = Form(default=None),
    price: Optional[int] = Form(default=None),
    post_type: Optional[str] = Form(default=None),
    available_quantity: Optional[int] = Form(default=None),
    location: Optional[str] = Form(default=None),
    category_id: Optional[int] = Form(default=None),
    controller: PostController = Depends(get_post_controller),
    user: UserView = Depends(auth.get_logged_user),
):
    body = PostUpdateWithImage(
        title=title,
        image=image,
        description=description,
        price=price,
        post_type=post_type,
        available_quantity=available_quantity,
        location=location,
        category_id=category_id,
    )
    return controller.update(post_id, body, user.id)


@posts.get(
    "/posts/highlights/",
    tags=["posts"],
    description="List top 5 viewed posts",
    response_model=List[PostView],
)
def list_highlight_posts(
    controller: PostController = Depends(get_post_controller),
):
    return controller.get_top_5_viewed_posts()


@posts.delete("/posts/{post_id}", tags=["posts"])
def delete_post(
    post_id: int,
    controller: PostController = Depends(get_post_controller),
    user: PostView = Depends(auth.get_logged_user),
):
    return controller.delete(post_id, user.id)
