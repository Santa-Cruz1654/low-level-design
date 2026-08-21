from domain.enums import GatewayType

from .base import PaymentGateway
from .paytm import PaytmGateway
from .razorpay import RazorpayGateway


class GatewayFactory:

    def create(
        self,
        gateway_type: GatewayType,
    ) -> PaymentGateway:

        if gateway_type == GatewayType.PAYTM:
            return PaytmGateway()

        if gateway_type == GatewayType.RAZORPAY:
            return RazorpayGateway()

        raise ValueError(
            f"Unsupported gateway: {gateway_type}"
        )