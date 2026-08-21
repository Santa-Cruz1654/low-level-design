from uuid import uuid4

from domain.enums import (
    EventType,
    PaymentStatus,
    ProviderResultStatus,
    ReconciliationStatus,
)
from domain.outbox import OutboxEvent
from domain.state_machine import PaymentStateMachine

from gateways.factory import GatewayFactory


class ReconciliationService:

    def __init__(
        self,
        unit_of_work,
        gateway_factory: GatewayFactory,
    ):
        self.unit_of_work = unit_of_work
        self.gateway_factory = gateway_factory

    def reconcile_unknown_payments(self) -> None:

        # -------------------------------------------------
        # Find all payments whose final outcome is unknown
        # -------------------------------------------------

        with self.unit_of_work as uow:

            unknown_payments = (
                uow.payments.get_unknown_payments()
            )

        print(
            f"[Reconciliation] "
            f"Found {len(unknown_payments)} "
            f"unknown payment(s)."
        )

        for payment in unknown_payments:

            try:
                self.reconcile_payment(
                    payment.payment_id
                )

            except Exception as exc:

                print(
                    f"[Reconciliation] "
                    f"Failed to reconcile "
                    f"{payment.payment_id}: "
                    f"{exc}"
                )

    def reconcile_payment(
        self,
        payment_id: str,
    ) -> None:

        # -------------------------------------------------
        # STEP 1
        # Load payment
        # -------------------------------------------------

        with self.unit_of_work as uow:

            payment = uow.payments.get_by_id(
                payment_id
            )

            if payment is None:
                print(
                    f"[Reconciliation] "
                    f"Payment {payment_id} "
                    f"not found."
                )
                return

            if (
                payment.status
                != PaymentStatus.UNKNOWN
            ):

                print(
                    f"[Reconciliation] "
                    f"Payment {payment_id} "
                    f"is not UNKNOWN. "
                    f"Skipping."
                )

                return

            # -------------------------------------------------
            # Mark reconciliation as IN_PROGRESS
            # -------------------------------------------------

            payment.reconciliation_status = (
                ReconciliationStatus.IN_PROGRESS
            )

            payment.update_timestamp()

            uow.payments.save(payment)

            uow.commit()

        # -------------------------------------------------
        # STEP 2
        # Ask external provider
        # -------------------------------------------------

        gateway = self.gateway_factory.create(
            payment.request.gateway_type
        )

        print(
            f"[Reconciliation] "
            f"Checking provider for "
            f"{payment_id}..."
        )

        result = gateway.get_payment_status(
            payment
        )

        # -------------------------------------------------
        # STEP 3
        # Resolve the UNKNOWN state
        # -------------------------------------------------

        self._apply_reconciliation_result(
            payment_id,
            result,
        )

    def _apply_reconciliation_result(
        self,
        payment_id: str,
        result,
    ) -> None:

        with self.unit_of_work as uow:

            payment = uow.payments.get_by_id(
                payment_id
            )

            if payment is None:
                return

            # -------------------------------------------------
            # Provider says SUCCESS
            # -------------------------------------------------

            if (
                result.status
                == ProviderResultStatus.SUCCESS
            ):

                PaymentStateMachine.transition(
                    payment.status,
                    PaymentStatus.SUCCESS,
                )

                uow.payments.update_status(
                    payment,
                    PaymentStatus.SUCCESS,
                    provider_transaction_id=(
                        result.provider_transaction_id
                    ),
                )

                payment.reconciliation_status = (
                    ReconciliationStatus.COMPLETED
                )

                event = OutboxEvent(
                    event_id=str(uuid4()),
                    event_type=(
                        EventType.PAYMENT_RECONCILED.value
                    ),
                    aggregate_id=payment.payment_id,
                    payload={
                        "payment_id": (
                            payment.payment_id
                        ),
                        "final_status": (
                            PaymentStatus.SUCCESS.value
                        ),
                        "provider_transaction_id": (
                            payment.provider_transaction_id
                        ),
                    },
                )

                uow.outbox.add(event)

                uow.commit()

                print(
                    f"[Reconciliation] "
                    f"{payment_id} resolved → SUCCESS"
                )

                return

            # -------------------------------------------------
            # Provider says FAILED
            # -------------------------------------------------

            if (
                result.status
                == ProviderResultStatus.FAILED
            ):

                PaymentStateMachine.transition(
                    payment.status,
                    PaymentStatus.FAILED,
                )

                uow.payments.update_status(
                    payment,
                    PaymentStatus.FAILED,
                    failure_reason=(
                        result.failure_reason
                    ),
                )

                payment.reconciliation_status = (
                    ReconciliationStatus.COMPLETED
                )

                event = OutboxEvent(
                    event_id=str(uuid4()),
                    event_type=(
                        EventType.PAYMENT_RECONCILED.value
                    ),
                    aggregate_id=payment.payment_id,
                    payload={
                        "payment_id": (
                            payment.payment_id
                        ),
                        "final_status": (
                            PaymentStatus.FAILED.value
                        ),
                        "failure_reason": (
                            payment.failure_reason
                        ),
                    },
                )

                uow.outbox.add(event)

                uow.commit()

                print(
                    f"[Reconciliation] "
                    f"{payment_id} resolved → FAILED"
                )

                return

            # -------------------------------------------------
            # Provider still cannot determine outcome
            # -------------------------------------------------

            if (
                result.status
                == ProviderResultStatus.UNKNOWN
            ):

                payment.reconciliation_status = (
                    ReconciliationStatus.PENDING
                )

                payment.update_timestamp()

                uow.payments.save(payment)

                uow.commit()

                print(
                    f"[Reconciliation] "
                    f"{payment_id} remains UNKNOWN."
                )

                return

            raise ValueError(
                f"Unsupported reconciliation "
                f"result: {result.status}"
            )