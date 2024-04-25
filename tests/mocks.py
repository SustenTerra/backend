from unittest.mock import Mock

import pytest
import stripe

from app.service.stripe_client import StripeClient


@pytest.fixture
def make_stripe_client_mock():
    def _make_stripe_client_mock():
        stripe_client_mock = Mock(spec=StripeClient)

        mocked_product = Mock(spec=stripe.Product)
        mocked_product.id = "prod_123"
        mocked_product.default_price = "price_123"

        stripe_client_mock.create_product.return_value = mocked_product
        stripe_client_mock.update_product.return_value = mocked_product

        mocked_payment_link = Mock(spec=stripe.PaymentLink)
        mocked_payment_link.url = "https://stripe.com/link"

        stripe_client_mock.create_payment_link.return_value = mocked_payment_link

        return stripe_client_mock

    return _make_stripe_client_mock
