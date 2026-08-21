import random
from uuid import uuid4

from domain.entities import Payment
from domain.enums import ProviderResultStatus
from domain.exceptions import PaymentValidationException
from domain.gateway_models import GatewayPaymentResult

from .base import PaymentGateway


class RazorpayGateway(PaymentGateway):

    def validate(
        self,
        payment: Payment,
    ) -> None:

        if payment.request.amount <= 0:
            raise PaymentValidationException(
                "Amount must be greater than zero."
            )

    def initiate(
        self,
        payment: Payment,
    ) -> GatewayPaymentResult:

        print(
            f"[Razorpay] Initiating "
            f"{payment.payment_id}"
        )

        result = random.randint(1, 100)

        if result <= 80:
            return GatewayPaymentResult(
                status=ProviderResultStatus.SUCCESS,
                provider_transaction_id=(
                    f"RZP-{uuid4().hex[:10]}"
                ),
            )

        if result <= 90:
            return GatewayPaymentResult(
                status=ProviderResultStatus.FAILED,
                failure_reason=(
                    "Razorpay declined payment."
                ),
            )

        return GatewayPaymentResult(
            status=ProviderResultStatus.UNKNOWN,
            retryable=True,
        )

    def confirm(
        self,
        payment: Payment,
        result: GatewayPaymentResult,
    ) -> GatewayPaymentResult:

        print(
            f"[Razorpay] Confirming "
            f"{payment.payment_id}"
        )

        return result

    def get_payment_status(
        self,
        payment: Payment,
    ) -> GatewayPaymentResult:

        print(
            f"[Razorpay] Reconciliation lookup "
            f"for {payment.payment_id}"
        )

        result = random.randint(1, 100)

        if result <= 75:
            return GatewayPaymentResult(
                status=ProviderResultStatus.SUCCESS,
                provider_transaction_id=(
                    f"RZP-{uuid4().hex[:10]}"
                ),
            )

        return GatewayPaymentResult(
            status=ProviderResultStatus.FAILED,
            failure_reason=(
                "Provider reports payment failed."
            ),
        )