from fastapi import Depends
from sqlalchemy.orm import Session

from app.deps import get_bucket_manager, get_session, get_stripe_client
from app.marketplace.post.controller import PostController
from app.marketplace.post.repository import PostRepository
from app.models import Post
from app.service.bucket_manager import BucketManager
from app.service.stripe_client import StripeClient


def get_post_repository(session: Session = Depends(get_session)):
    return PostRepository(Post, session)


def get_post_controller(
    repository: PostRepository = Depends(get_post_repository),
    bucket_manager: BucketManager = Depends(get_bucket_manager),
    stripe_client: StripeClient = Depends(get_stripe_client),
):
    return PostController(Post, repository, bucket_manager, stripe_client)
