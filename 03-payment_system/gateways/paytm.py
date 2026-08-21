import random
from uuid import uuid4

from domain.entities import Payment
from domain.enums import ProviderResultStatus
from domain.exceptions import PaymentValidationException
from domain.gateway_models import GatewayPaymentResult

from .base import PaymentGateway


class PaytmGateway(PaymentGateway):

    def validate(
        self,
        payment: Payment,
    ) -> None:

        if payment.request.amount <= 0:
            raise PaymentValidationException(
                "Amount must be greater than zero."
            )

        if payment.request.currency != "INR":
            raise PaymentValidationException(
                "Paytm supports INR in this simulation."
            )

    def initiate(
        self,
        payment: Payment,
    ) -> GatewayPaymentResult:

        print(
            f"[Paytm] Initiating "
            f"{payment.payment_id}"
        )

        result = random.randint(1, 100)

        if result <= 70:
            return GatewayPaymentResult(
                status=ProviderResultStatus.SUCCESS,
                provider_transaction_id=(
                    f"PTM-{uuid4().hex[:10]}"
                ),
            )

        if result <= 85:
            return GatewayPaymentResult(
                status=ProviderResultStatus.FAILED,
                failure_reason=(
                    "Provider declined payment."
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
            f"[Paytm] Confirming "
            f"{payment.payment_id}"
        )

        return result

    def get_payment_status(
        self,
        payment: Payment,
    ) -> GatewayPaymentResult:

        print(
            f"[Paytm] Reconciliation lookup "
            f"for {payment.payment_id}"
        )

        result = random.randint(1, 100)

        if result <= 70:
            return GatewayPaymentResult(
                status=ProviderResultStatus.SUCCESS,
                provider_transaction_id=(
                    f"PTM-{uuid4().hex[:10]}"
                ),
            )

        return GatewayPaymentResult(
            status=ProviderResultStatus.FAILED,
            failure_reason=(
                "Provider reports payment failed."
            ),
        )