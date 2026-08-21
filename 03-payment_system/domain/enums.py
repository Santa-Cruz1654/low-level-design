from enum import Enum


class PaymentStatus(Enum):
    CREATED = "CREATED"
    PROCESSING = "PROCESSING"
    SUCCESS = "SUCCESS"
    FAILED = "FAILED"
    UNKNOWN = "UNKNOWN"


class ReconciliationStatus(Enum):
    NOT_REQUIRED = "NOT_REQUIRED"
    PENDING = "PENDING"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"


class GatewayType(Enum):
    PAYTM = "PAYTM"
    RAZORPAY = "RAZORPAY"


class ProviderResultStatus(Enum):
    SUCCESS = "SUCCESS"
    FAILED = "FAILED"
    UNKNOWN = "UNKNOWN"


class EventType(Enum):
    PAYMENT_CREATED = "PaymentCreated"
    PAYMENT_SUCCEEDED = "PaymentSucceeded"
    PAYMENT_FAILED = "PaymentFailed"
    PAYMENT_UNKNOWN = "PaymentUnknown"
    PAYMENT_RECONCILED = "PaymentReconciled"