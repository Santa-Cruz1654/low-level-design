from application.commands import ProcessPaymentCommand
from domain.enums import (
    GatewayType,
)


def test_duplicate_request_returns_same_payment(
    controller,
):

    command = ProcessPaymentCommand(
        sender="Aditya",
        receiver="Shubham",
        amount=1000.0,
        currency="INR",
        idempotency_key="IDEMPOTENCY-001",
        gateway_type=GatewayType.PAYTM,
    )

    first_payment = controller.handle_payment(
        command
    )

    second_payment = controller.handle_payment(
        command
    )

    assert (
        first_payment.payment_id
        == second_payment.payment_id
    )