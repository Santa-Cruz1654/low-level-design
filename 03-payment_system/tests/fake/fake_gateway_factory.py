from gateways.base import PaymentGateway


class FakeGatewayFactory:
    """
    Test-only gateway factory.

    Always returns the gateway supplied during construction,
    regardless of GatewayType.
    """

    def __init__(
        self,
        gateway: PaymentGateway,
    ):
        self.gateway = gateway

    def create(
        self,
        gateway_type,
    ) -> PaymentGateway:

        return self.gateway