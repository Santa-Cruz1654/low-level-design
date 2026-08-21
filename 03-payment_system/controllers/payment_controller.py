from application.commands import ProcessPaymentCommand
from application.services import PaymentService


class PaymentController:

    def __init__(
        self,
        payment_service: PaymentService,
    ):
        self.payment_service = payment_service

    def handle_payment(
        self,
        command: ProcessPaymentCommand,
    ):

        print(
            "\n[Controller] "
            "Received payment request."
        )

        payment = (
            self.payment_service.process_payment(
                command
            )
        )

        print(
            f"[Controller] "
            f"Payment {payment.payment_id} "
            f"→ {payment.status.value}"
        )

        return payment