from typing import Optional

import stripe

from app.config import Config
from app.marketplace.post.schema import PostUpdate
from app.models import Post


class StripeClient:
    DEFAULT_CURRENCY = "brl"

    def __init__(self) -> None:
        self.config = Config()
        self.client = stripe.StripeClient(api_key=self.config.STRIPE_API_KEY)

    def create_product(
        self, name: str, description: str, price: int
    ) -> Optional[stripe.Product]:
        price_params = stripe.ProductService.CreateParamsDefaultPriceData(
            currency="brl", unit_amount=price
        )

        params = stripe.ProductService.CreateParams(
            name=name,
            default_price_data=price_params,
            description=description,
        )

        return self.client.products.create(params=params)

    def create_price(self, price_value: int, stripe_product_id: str) -> stripe.Price:
        price_params = stripe.PriceService.CreateParams(
            currency=self.DEFAULT_CURRENCY,
            unit_amount=price_value,
            product=stripe_product_id,
        )

        return self.client.prices.create(price_params)

    def update_product(
        self, update_body: PostUpdate, post: Post
    ) -> Optional[stripe.Product]:
        if post.price is None or post.stripe_product_id is None:
            return

        values_to_update = dict()

        if update_body.title is not None:
            values_to_update["name"] = update_body.title

        if update_body.description is not None:
            values_to_update["description"] = update_body.description

        if update_body.price is not None:
            price = self.create_price(update_body.price, post.stripe_product_id)
            values_to_update["default_price"] = price.id

        if not values_to_update:
            return

        update_params = stripe.ProductService.UpdateParams(**values_to_update)
        return self.client.products.update(post.stripe_product_id, update_params)

    def create_payment_link(self, post: Post) -> Optional[stripe.PaymentLink]:
        if post.stripe_product_id is None or post.stripe_price_id is None:
            return

        create_params = stripe.PaymentLinkService.CreateParams(
            line_items=[
                stripe.PaymentLinkService.CreateParamsLineItem(
                    price=post.stripe_price_id, quantity=1
                )
            ],
            after_completion=stripe.PaymentLinkService.CreateParamsAfterCompletion(
                type="redirect",
                redirect=stripe.PaymentLinkService.CreateParamsAfterCompletionRedirect(
                    url=f"{self.config.WEBSITE_URL}/profile/my-orders"
                ),
            ),
            metadata={"post_id": str(post.id), "user_id": str(post.user.id)},
        )

        return self.client.payment_links.create(create_params)
