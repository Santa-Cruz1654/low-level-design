from application.commands import ProcessPaymentCommand
from domain.enums import (
    GatewayType,
    PaymentStatus,
)


def test_invalid_payment_fails(
    controller,
):

    command = ProcessPaymentCommand(
        sender="Aditya",
        receiver="Shubham",
        amount=0,
        currency="INR",
        idempotency_key="FAIL-001",
        gateway_type=GatewayType.PAYTM,
    )

    payment = controller.handle_payment(
        command
    )

    assert payment.status == PaymentStatus.FAILED