from abc import ABC, abstractmethod

from domain.entities import Payment
from domain.gateway_models import GatewayPaymentResult


class PaymentGateway(ABC):

    @abstractmethod
    def validate(
        self,
        payment: Payment,
    ) -> None:
        pass

    @abstractmethod
    def initiate(
        self,
        payment: Payment,
    ) -> GatewayPaymentResult:
        pass

    @abstractmethod
    def confirm(
        self,
        payment: Payment,
        result: GatewayPaymentResult,
    ) -> GatewayPaymentResult:
        pass

    @abstractmethod
    def get_payment_status(
        self,
        payment: Payment,
    ) -> GatewayPaymentResult:
        pass

    def process(
        self,
        payment: Payment,
    ) -> GatewayPaymentResult:

        self.validate(payment)

        result = self.initiate(payment)

        if result.status.value == "UNKNOWN":
            return result

        return self.confirm(
            payment,
            result,
        )