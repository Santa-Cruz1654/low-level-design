from dataclasses import dataclass
from typing import Optional

from .enums import ProviderResultStatus


@dataclass(frozen=True)
class GatewayPaymentResult:
    status: ProviderResultStatus

    provider_transaction_id: Optional[str] = None

    failure_reason: Optional[str] = None

    retryable: bool = False