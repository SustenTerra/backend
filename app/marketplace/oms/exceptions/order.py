from typing import Optional

from fastapi import HTTPException


class NotAvailableForOrderException(HTTPException):
    def __init__(self, detail: Optional[str] = None):
        super().__init__(status_code=400, detail=detail or "Not available for order.")


class CouldNotCreatePaymentLinkException(HTTPException):
    def __init__(self, detail: Optional[str] = None):
        super().__init__(
            status_code=400, detail=detail or "Could not create payment link."
        )
