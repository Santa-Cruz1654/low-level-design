class PaymentException(Exception):
    """Base exception for payment-related errors."""


class PaymentValidationException(PaymentException):
    """Raised when payment input is invalid."""


class PaymentNotFoundException(PaymentException):
    """Raised when a payment cannot be found."""


class InvalidPaymentStateException(PaymentException):
    """Raised when an illegal state transition is attempted."""


class ConcurrentModificationException(PaymentException):
    """Raised when optimistic locking detects a stale version."""


class GatewayException(PaymentException):
    """Base exception for external gateway failures."""


class ProviderTimeoutException(GatewayException):
    """Raised when the provider times out."""


class ProviderUnavailableException(GatewayException):
    """Raised when the provider is unavailable."""


class ReconciliationException(PaymentException):
    """Raised when reconciliation fails."""