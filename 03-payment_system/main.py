from application.commands import ProcessPaymentCommand
from application.reconciliation import ReconciliationService
from application.retry import RetryExecutor
from application.retry_policy import RetryPolicy
from application.services import PaymentService

from controllers.payment_controller import PaymentController

from domain.enums import GatewayType

from gateways.factory import GatewayFactory

from messaging.in_memory_publisher import (
    InMemoryEventPublisher,
)
from messaging.outbox_publisher import (
    OutboxPublisher,
)

from repositories.in_memory_unit_of_work import (
    InMemoryUnitOfWork,
)


def build_application():

    # =====================================================
    # INFRASTRUCTURE
    # =====================================================

    unit_of_work = InMemoryUnitOfWork()

    gateway_factory = GatewayFactory()

    publisher = InMemoryEventPublisher()

    # =====================================================
    # RETRY
    # =====================================================

    retry_policy = RetryPolicy(
        max_attempts=3,
        initial_delay_seconds=0.5,
        max_delay_seconds=2.0,
        backoff_multiplier=2.0,
    )

    retry_executor = RetryExecutor(
        retry_policy
    )

    # =====================================================
    # APPLICATION SERVICES
    # =====================================================

    payment_service = PaymentService(
        unit_of_work=unit_of_work,
        gateway_factory=gateway_factory,
        retry_executor=retry_executor,
    )

    reconciliation_service = (
        ReconciliationService(
            unit_of_work=unit_of_work,
            gateway_factory=gateway_factory,
        )
    )

    # =====================================================
    # CONTROLLER
    # =====================================================

    controller = PaymentController(
        payment_service
    )

    # =====================================================
    # OUTBOX PUBLISHER
    # =====================================================

    outbox_publisher = OutboxPublisher(
        unit_of_work=unit_of_work,
        publisher=publisher,
    )

    return (
        controller,
        reconciliation_service,
        outbox_publisher,
        publisher,
        unit_of_work,
    )


def main():

    (
        controller,
        reconciliation_service,
        outbox_publisher,
        publisher,
        unit_of_work,
    ) = build_application()

    # =====================================================
    # PAYMENT 1
    # =====================================================

    print("\n" + "=" * 60)
    print("PAYMENT 1 — PAYTM")
    print("=" * 60)

    command_1 = ProcessPaymentCommand(
        sender="Aditya",
        receiver="Shubham",
        amount=1000.0,
        currency="INR",
        idempotency_key="PAYMENT-001",
        gateway_type=GatewayType.PAYTM,
    )

    payment_1 = controller.handle_payment(
        command_1
    )

    # =====================================================
    # PAYMENT 2
    # =====================================================

    print("\n" + "=" * 60)
    print("PAYMENT 2 — RAZORPAY")
    print("=" * 60)

    command_2 = ProcessPaymentCommand(
        sender="Shubham",
        receiver="Aditya",
        amount=500.0,
        currency="INR",
        idempotency_key="PAYMENT-002",
        gateway_type=GatewayType.RAZORPAY,
    )

    payment_2 = controller.handle_payment(
        command_2
    )

    # =====================================================
    # IDEMPOTENCY TEST
    # =====================================================

    print("\n" + "=" * 60)
    print("IDEMPOTENCY TEST")
    print("=" * 60)

    duplicate_payment = controller.handle_payment(
        command_1
    )

    print(
        "\nOriginal payment ID :",
        payment_1.payment_id,
    )

    print(
        "Duplicate payment ID:",
        duplicate_payment.payment_id,
    )

    print(
        "Same payment object:",
        payment_1.payment_id
        == duplicate_payment.payment_id,
    )

    # =====================================================
    # OUTBOX PUBLISHING
    # =====================================================

    print("\n" + "=" * 60)
    print("PUBLISH OUTBOX EVENTS")
    print("=" * 60)

    outbox_publisher.publish_pending_events()

    print(
        "\nPublished events:",
        len(publisher.published_events),
    )

    for event in publisher.published_events:

        print(
            f"  - {event.event_type} "
            f"for payment "
            f"{event.aggregate_id}"
        )

    # =====================================================
    # RECONCILIATION
    # =====================================================

    print("\n" + "=" * 60)
    print("RECONCILIATION")
    print("=" * 60)

    reconciliation_service.reconcile_unknown_payments()

    # =====================================================
    # PUBLISH EVENTS CREATED BY RECONCILIATION
    # =====================================================

    print("\n" + "=" * 60)
    print("PUBLISH RECONCILIATION EVENTS")
    print("=" * 60)

    outbox_publisher.publish_pending_events()

    # =====================================================
    # FINAL PAYMENT STATES
    # =====================================================

    print("\n" + "=" * 60)
    print("FINAL PAYMENT STATES")
    print("=" * 60)

    for payment in unit_of_work.payments.payments.values():

        print(
            f"\nPayment ID: "
            f"{payment.payment_id}"
        )

        print(
            f"Status: "
            f"{payment.status.value}"
        )

        print(
            f"Gateway: "
            f"{payment.request.gateway_type.value}"
        )

        print(
            f"Amount: "
            f"{payment.request.amount} "
            f"{payment.request.currency}"
        )

        print(
            f"Provider Transaction ID: "
            f"{payment.provider_transaction_id}"
        )

        print(
            f"Reconciliation: "
            f"{payment.reconciliation_status.value}"
        )


if __name__ == "__main__":
    main()