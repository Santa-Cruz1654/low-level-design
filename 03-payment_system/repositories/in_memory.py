from typing import Optional

from domain.entities import Payment
from domain.enums import (
    PaymentStatus,
    ReconciliationStatus,
)
from domain.exceptions import (
    ConcurrentModificationException,
)

from .base import PaymentRepository


class InMemoryPaymentRepository(
    PaymentRepository
):

    def __init__(self):

        self.payments: dict[str, Payment] = {}

    def save(
        self,
        payment: Payment,
    ) -> None:

        self.payments[
            payment.payment_id
        ] = payment

    def get_by_id(
        self,
        payment_id: str,
    ) -> Optional[Payment]:

        return self.payments.get(payment_id)

    def get_by_idempotency_key(
        self,
        idempotency_key: str,
    ) -> Optional[Payment]:

        for payment in self.payments.values():

            if (
                payment.request.idempotency_key
                == idempotency_key
            ):
                return payment

        return None

    def update_status(
        self,
        payment: Payment,
        new_status: PaymentStatus,
        provider_transaction_id=None,
        failure_reason=None,
    ) -> None:

        stored = self.payments.get(
            payment.payment_id
        )

        if stored is None:
            raise KeyError(
                f"Payment not found: "
                f"{payment.payment_id}"
            )

        if stored.version != payment.version:
            raise ConcurrentModificationException(
                f"Concurrent modification detected "
                f"for {payment.payment_id}"
            )

        payment.status = new_status

        if provider_transaction_id is not None:
            payment.provider_transaction_id = (
                provider_transaction_id
            )

        if failure_reason is not None:
            payment.failure_reason = (
                failure_reason
            )

        if new_status == PaymentStatus.UNKNOWN:

            payment.reconciliation_status = (
                ReconciliationStatus.PENDING
            )

        elif new_status in {
            PaymentStatus.SUCCESS,
            PaymentStatus.FAILED,
        }:

            payment.reconciliation_status = (
                ReconciliationStatus.NOT_REQUIRED
            )

        payment.version += 1

        payment.update_timestamp()

        self.payments[
            payment.payment_id
        ] = payment

    def get_unknown_payments(
        self,
    ) -> list[Payment]:

        return [
            payment
            for payment in self.payments.values()
            if payment.status
            == PaymentStatus.UNKNOWN
        ]