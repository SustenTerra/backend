import stripe

from app.config import Config
from app.marketplace.oms.controllers.order import OrderController
from app.marketplace.oms.schemas.stripe import CheckoutSession


class StripeWebhookController:
    def __init__(self, order_controller: OrderController) -> None:
        self.order_controller = order_controller
        self.config = Config()

    def handle_event(self, signature_header: str, body: bytes):
        event = None
        try:
            event = stripe.Webhook.construct_event(
                body, signature_header, self.config.STRIPE_ENDPOINT_SECRET
            )
        except ValueError as e:
            raise e
        except stripe.SignatureVerificationError as e:
            raise e

        if event.type == "checkout.session.completed":
            checkout_session = CheckoutSession(**event.data.object)
            print(checkout_session)
