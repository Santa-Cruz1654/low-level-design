from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Optional

from .enums import (
    GatewayType,
    PaymentStatus,
    ReconciliationStatus,
)


@dataclass(frozen=True)
class PaymentRequest:
    sender: str
    receiver: str
    amount: float
    currency: str
    idempotency_key: str
    gateway_type: GatewayType


@dataclass
class Payment:
    payment_id: str
    request: PaymentRequest

    status: PaymentStatus = PaymentStatus.CREATED

    provider_transaction_id: Optional[str] = None

    failure_reason: Optional[str] = None

    reconciliation_status: ReconciliationStatus = (
        ReconciliationStatus.NOT_REQUIRED
    )

    version: int = 0

    created_at: datetime = field(
        default_factory=lambda: datetime.now(timezone.utc)
    )

    updated_at: datetime = field(
        default_factory=lambda: datetime.now(timezone.utc)
    )

    def update_timestamp(self) -> None:
        self.updated_at = datetime.now(timezone.utc)