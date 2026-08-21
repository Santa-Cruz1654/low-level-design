from domain.gateway_models import GatewayPaymentResult

from gateways.base import PaymentGateway


class FakePaymentGateway(PaymentGateway):
    """
    Deterministic gateway used by tests.

    The test controls exactly what the provider returns.
    There is no randomness and no external dependency.
    """

    def __init__(
        self,
        result: GatewayPaymentResult,
    ):
        self.result = result

    def validate(self, payment) -> None:
        """
        Validation is intentionally successful.

        Validation behavior is tested separately through
        the real gateway.
        """
        pass

    def initiate(
        self,
        payment,
    ) -> GatewayPaymentResult:

        return self.result

    def confirm(
        self,
        payment,
        result: GatewayPaymentResult,
    ) -> GatewayPaymentResult:

        return result

    def get_payment_status(
        self,
        payment,
    ) -> GatewayPaymentResult:

        return self.result