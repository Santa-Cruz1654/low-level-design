from abc import ABC, abstractmethod
from typing import Optional

from domain.entities import Payment
from domain.enums import PaymentStatus


class PaymentRepository(ABC):

    @abstractmethod
    def save(
        self,
        payment: Payment,
    ) -> None:
        pass

    @abstractmethod
    def get_by_id(
        self,
        payment_id: str,
    ) -> Optional[Payment]:
        pass

    @abstractmethod
    def get_by_idempotency_key(
        self,
        idempotency_key: str,
    ) -> Optional[Payment]:
        pass

    @abstractmethod
    def update_status(
        self,
        payment: Payment,
        new_status: PaymentStatus,
        provider_transaction_id=None,
        failure_reason=None,
    ) -> None:
        pass

    @abstractmethod
    def get_unknown_payments(
        self,
    ) -> list[Payment]:
        pass