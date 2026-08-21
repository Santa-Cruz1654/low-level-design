from uuid import uuid4

from domain.entities import Payment, PaymentRequest
from domain.enums import (
    EventType,
    PaymentStatus,
    ProviderResultStatus,
)
from domain.exceptions import PaymentValidationException
from domain.gateway_models import GatewayPaymentResult
from domain.outbox import OutboxEvent
from domain.state_machine import PaymentStateMachine

from gateways.factory import GatewayFactory

from .commands import ProcessPaymentCommand
from .retry import RetryExecutor


class PaymentService:

    def __init__(
        self,
        unit_of_work,
        gateway_factory: GatewayFactory,
        retry_executor: RetryExecutor,
    ):
        self.unit_of_work = unit_of_work
        self.gateway_factory = gateway_factory
        self.retry_executor = retry_executor

    def process_payment(
        self,
        command: ProcessPaymentCommand,
    ) -> Payment:

        # -------------------------------------------------
        # 1. IDEMPOTENCY CHECK
        # -------------------------------------------------

        with self.unit_of_work as uow:

            existing_payment = (
                uow.payments.get_by_idempotency_key(
                    command.idempotency_key
                )
            )

            if existing_payment is not None:

                print(
                    "[PaymentService] "
                    "Duplicate request detected."
                )

                return existing_payment

            # -------------------------------------------------
            # 2. CREATE PAYMENT REQUEST
            # -------------------------------------------------

            request = PaymentRequest(
                sender=command.sender,
                receiver=command.receiver,
                amount=command.amount,
                currency=command.currency,
                idempotency_key=(
                    command.idempotency_key
                ),
                gateway_type=command.gateway_type,
            )

            # -------------------------------------------------
            # 3. CREATE PAYMENT ENTITY
            # -------------------------------------------------

            payment = Payment(
                payment_id=str(uuid4()),
                request=request,
            )

            print(
                f"[PaymentService] "
                f"Created payment "
                f"{payment.payment_id}"
            )

            # -------------------------------------------------
            # 4. SAVE CREATED PAYMENT
            # -------------------------------------------------

            uow.payments.save(payment)

            # -------------------------------------------------
            # 5. CREATE PAYMENT CREATED EVENT
            # -------------------------------------------------

            event = self._create_event(
                EventType.PAYMENT_CREATED,
                payment,
            )

            uow.outbox.add(event)

            uow.commit()

        # -------------------------------------------------
        # 6. PROCESS THE PAYMENT
        # -------------------------------------------------

        return self._execute_payment(
            payment.payment_id
        )

    # =========================================================
    # PAYMENT EXECUTION
    # =========================================================

    def _execute_payment(
        self,
        payment_id: str,
    ) -> Payment:

        with self.unit_of_work as uow:

            payment = uow.payments.get_by_id(
                payment_id
            )

            if payment is None:
                raise ValueError(
                    f"Payment not found: "
                    f"{payment_id}"
                )

            # -------------------------------------------------
            # Move CREATED → PROCESSING
            # -------------------------------------------------

            PaymentStateMachine.transition(
                payment.status,
                PaymentStatus.PROCESSING,
            )

            uow.payments.update_status(
                payment,
                PaymentStatus.PROCESSING,
            )

            uow.commit()

        # -------------------------------------------------
        # Get gateway
        # -------------------------------------------------

        gateway = self.gateway_factory.create(
            payment.request.gateway_type
        )

        # -------------------------------------------------
        # Call external provider
        # -------------------------------------------------

        try:

            result = self.retry_executor.execute(
                lambda: gateway.process(payment)
            )

        # -------------------------------------------------
        # BUSINESS / VALIDATION FAILURE
        # -------------------------------------------------
        #
        # We know exactly what went wrong.
        #
        # Therefore:
        #
        # PaymentValidationException
        #              ↓
        #           FAILED
        #
        # We MUST NOT classify this as UNKNOWN.
        # -------------------------------------------------

        except PaymentValidationException as exc:

            return self._handle_validation_failure(
                payment_id,
                str(exc),
            )

        # -------------------------------------------------
        # INFRASTRUCTURE / UNKNOWN FAILURE
        # -------------------------------------------------
        #
        # We cannot determine whether the provider
        # processed the payment.
        #
        # Therefore:
        #
        # Provider timeout / connection failure / etc.
        #              ↓
        #           UNKNOWN
        #
        # Reconciliation can resolve it later.
        # -------------------------------------------------

        except Exception as exc:

            return self._handle_gateway_exception(
                payment_id,
                str(exc),
            )

        # -------------------------------------------------
        # Handle provider result
        # -------------------------------------------------

        return self._handle_gateway_result(
            payment_id,
            result,
        )

    # =========================================================
    # PROVIDER RESULT
    # =========================================================

    def _handle_gateway_result(
        self,
        payment_id: str,
        result: GatewayPaymentResult,
    ) -> Payment:

        with self.unit_of_work as uow:

            payment = uow.payments.get_by_id(
                payment_id
            )

            if payment is None:
                raise ValueError(
                    f"Payment not found: "
                    f"{payment_id}"
                )

            # -------------------------------------------------
            # SUCCESS
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

                event = self._create_event(
                    EventType.PAYMENT_SUCCEEDED,
                    payment,
                )

                uow.outbox.add(event)

                uow.commit()

                print(
                    f"[PaymentService] "
                    f"Payment {payment_id} "
                    f"SUCCESS"
                )

                return payment

            # -------------------------------------------------
            # FAILED
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

                event = self._create_event(
                    EventType.PAYMENT_FAILED,
                    payment,
                )

                uow.outbox.add(event)

                uow.commit()

                print(
                    f"[PaymentService] "
                    f"Payment {payment_id} "
                    f"FAILED"
                )

                return payment

            # -------------------------------------------------
            # UNKNOWN
            # -------------------------------------------------

            if (
                result.status
                == ProviderResultStatus.UNKNOWN
            ):

                PaymentStateMachine.transition(
                    payment.status,
                    PaymentStatus.UNKNOWN,
                )

                uow.payments.update_status(
                    payment,
                    PaymentStatus.UNKNOWN,
                    failure_reason=(
                        "Provider outcome "
                        "could not be determined."
                    ),
                )

                event = self._create_event(
                    EventType.PAYMENT_UNKNOWN,
                    payment,
                )

                uow.outbox.add(event)

                uow.commit()

                print(
                    f"[PaymentService] "
                    f"Payment {payment_id} "
                    f"UNKNOWN"
                )

                return payment

            raise ValueError(
                f"Unsupported provider result: "
                f"{result.status}"
            )

    # =========================================================
    # VALIDATION FAILURE
    # =========================================================
    #
    # This is different from _handle_gateway_exception().
    #
    # Validation failure means:
    #
    # "We KNOW the payment cannot be processed."
    #
    # Therefore:
    #
    # PROCESSING → FAILED
    #
    # No reconciliation is required.
    # =========================================================

    def _handle_validation_failure(
        self,
        payment_id: str,
        reason: str,
    ) -> Payment:

        with self.unit_of_work as uow:

            payment = uow.payments.get_by_id(
                payment_id
            )

            if payment is None:
                raise ValueError(
                    f"Payment not found: "
                    f"{payment_id}"
                )

            PaymentStateMachine.transition(
                payment.status,
                PaymentStatus.FAILED,
            )

            uow.payments.update_status(
                payment,
                PaymentStatus.FAILED,
                failure_reason=reason,
            )

            event = self._create_event(
                EventType.PAYMENT_FAILED,
                payment,
            )

            uow.outbox.add(event)

            uow.commit()

            print(
                f"[PaymentService] "
                f"Payment {payment_id} "
                f"FAILED: {reason}"
            )

            return payment

    # =========================================================
    # GATEWAY EXCEPTION
    # =========================================================
    #
    # This represents an uncertain external outcome.
    #
    # Example:
    #
    # Payment request sent
    #        ↓
    # Provider processes it
    #        ↓
    # Network connection disappears
    #
    # We do NOT know whether the provider succeeded.
    #
    # Therefore:
    #
    # PROCESSING → UNKNOWN
    #
    # Later:
    #
    # UNKNOWN → reconciliation → SUCCESS / FAILED
    # =========================================================

    def _handle_gateway_exception(
        self,
        payment_id: str,
        reason: str,
    ) -> Payment:

        with self.unit_of_work as uow:

            payment = uow.payments.get_by_id(
                payment_id
            )

            if payment is None:
                raise ValueError(
                    f"Payment not found: "
                    f"{payment_id}"
                )

            PaymentStateMachine.transition(
                payment.status,
                PaymentStatus.UNKNOWN,
            )

            uow.payments.update_status(
                payment,
                PaymentStatus.UNKNOWN,
                failure_reason=reason,
            )

            event = self._create_event(
                EventType.PAYMENT_UNKNOWN,
                payment,
            )

            uow.outbox.add(event)

            uow.commit()

            print(
                f"[PaymentService] "
                f"Payment {payment_id} "
                f"UNKNOWN due to gateway error."
            )

            return payment

    # =========================================================
    # EVENT CREATION
    # =========================================================

    def _create_event(
        self,
        event_type: EventType,
        payment: Payment,
    ) -> OutboxEvent:

        return OutboxEvent(
            event_id=str(uuid4()),
            event_type=event_type.value,
            aggregate_id=payment.payment_id,
            payload={
                "payment_id": payment.payment_id,
                "status": payment.status.value,
                "sender": payment.request.sender,
                "receiver": payment.request.receiver,
                "amount": payment.request.amount,
                "currency": payment.request.currency,
                "gateway": (
                    payment.request.gateway_type.value
                ),
                "provider_transaction_id": (
                    payment.provider_transaction_id
                ),
                "failure_reason": (
                    payment.failure_reason
                ),
            },
        )