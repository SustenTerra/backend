from typing import Annotated, List, Optional

from fastapi import APIRouter, Depends, File, Form, UploadFile

from app.controllers.post import PostController
from app.deps import get_post_controller
from app.schemas.post import PostCreateWithImage, PostUpdate, PostView
from app.schemas.users import UserView
from app.services import auth

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
    controller: PostController = Depends(get_post_controller),
    user: UserView = Depends(auth.get_logged_user),
):
    body = PostCreateWithImage(
        title=title,
        image=image,
        description=description,
        price=price,
        post_type=post_type,
        location=location,
        category_id=category_id,
        user_id=user.id,
    )

    return controller.create(body)


@posts.get(
    "/posts",
    description="List all posts",
    response_model=List[PostView],
)
def list_all_posts(
    search_term: Optional[str] = None,
    user_id: Optional[int] = None,
    controller: PostController = Depends(get_post_controller),
):
    return controller.get_all(search_term, user_id)


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


@posts.patch("/posts/{post_id}", tags=["posts"], response_model=PostView)
def update_post(
    post_id: int,
    body: PostUpdate,
    controller: PostController = Depends(get_post_controller),
    user: PostView = Depends(auth.get_logged_user),
):
    return controller.update(post_id, body, user.id)


@posts.get(
    "/posts/highlights/",
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
