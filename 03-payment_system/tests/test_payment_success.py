from application.commands import ProcessPaymentCommand

from domain.enums import (
    GatewayType,
    PaymentStatus,
)


def test_successful_payment(
    successful_controller,
):

    command = ProcessPaymentCommand(
        sender="Aditya",
        receiver="Shubham",
        amount=1000.0,
        currency="INR",
        idempotency_key="SUCCESS-001",
        gateway_type=GatewayType.PAYTM,
    )

    payment = successful_controller.handle_payment(
        command
    )

    assert payment.status == PaymentStatus.SUCCESS

    assert (
        payment.provider_transaction_id
        == "TEST-TXN-001"
    )