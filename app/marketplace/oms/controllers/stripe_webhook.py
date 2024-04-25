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

            if not checkout_session.metadata:
                # TODO: send email to admin
                return

            if (
                not checkout_session.metadata.post_id
                or not checkout_session.metadata.user_id
            ):
                # TODO: send email to admin
                return

            self.order_controller.create(
                user_id=int(checkout_session.metadata.user_id),
                post_id=int(checkout_session.metadata.post_id),
            )
