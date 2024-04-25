from typing import Optional

import stripe

from app.config import Config
from app.marketplace.post.schema import PostCreate


class StripeClient:
    def __init__(self) -> None:
        self.config = Config()
        self.client = stripe.StripeClient(api_key=self.config.STRIPE_API_KEY)

    def create_product(self, post: PostCreate) -> Optional[stripe.Product]:
        if post.price is None:
            return None

        price_params = stripe.ProductService.CreateParamsDefaultPriceData(
            currency="brl", unit_amount=post.price
        )

        params = stripe.ProductService.CreateParams(
            name=post.title,
            default_price_data=price_params,
            description=post.description,
        )

        return self.client.products.create(params=params)
