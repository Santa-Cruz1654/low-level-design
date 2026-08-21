from application.commands import ProcessPaymentCommand

from domain.enums import (
    GatewayType,
    PaymentStatus,
    ReconciliationStatus,
)


def test_unknown_payment_is_reconciled(
    controller,
    reconciliation_service,
    unit_of_work,
):

    command = ProcessPaymentCommand(
        sender="Aditya",
        receiver="Shubham",
        amount=1000.0,
        currency="INR",
        idempotency_key="RECON-001",
        gateway_type=GatewayType.RAZORPAY,
    )

    payment = controller.handle_payment(
        command
    )

    # Force the scenario we want to test.
    # In production this state would normally
    # be produced by a timeout/uncertain provider result.
    payment.status = PaymentStatus.UNKNOWN
    payment.reconciliation_status = (
        ReconciliationStatus.PENDING
    )

    unit_of_work.payments.save(payment)

    reconciliation_service.reconcile_payment(
        payment.payment_id
    )

    updated_payment = (
        unit_of_work.payments.get_by_id(
            payment.payment_id
        )
    )

    assert updated_payment.status in (
        PaymentStatus.SUCCESS,
        PaymentStatus.FAILED,
    )

    assert (
        updated_payment.reconciliation_status
        == ReconciliationStatus.COMPLETED
    )