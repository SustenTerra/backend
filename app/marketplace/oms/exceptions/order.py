from typing import Optional


class NotAvailableForOrderException(Exception):
    def __init__(self, message: Optional[str] = None):
        self.message = message or "This product is not available for order."
