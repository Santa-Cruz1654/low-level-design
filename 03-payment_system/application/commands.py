from dataclasses import dataclass

from domain.enums import GatewayType


@dataclass(frozen=True)
class ProcessPaymentCommand:

    sender: str
    receiver: str
    amount: float
    currency: str

    idempotency_key: str

    gateway_type: GatewayType