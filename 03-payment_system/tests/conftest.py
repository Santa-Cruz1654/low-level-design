import pytest

from application.reconciliation import ReconciliationService
from application.retry import RetryExecutor
from application.retry_policy import RetryPolicy
from application.services import PaymentService
from controllers.payment_controller import PaymentController

from domain.gateway_models import GatewayPaymentResult
from domain.enums import ProviderResultStatus

from gateways.factory import GatewayFactory

from messaging.in_memory_publisher import (
    InMemoryEventPublisher,
)

from messaging.outbox_publisher import (
    OutboxPublisher,
)

from repositories.in_memory_unit_of_work import (
    InMemoryUnitOfWork,
)

from tests.fake.fake_gateway import (
    FakePaymentGateway,
)

from tests.fake.fake_gateway_factory import (
    FakeGatewayFactory,
)


@pytest.fixture
def unit_of_work():
    return InMemoryUnitOfWork()


@pytest.fixture
def gateway_factory():
    return GatewayFactory()


@pytest.fixture
def publisher():
    return InMemoryEventPublisher()


@pytest.fixture
def retry_executor():

    policy = RetryPolicy(
        max_attempts=3,
        initial_delay_seconds=0,
        max_delay_seconds=0,
        backoff_multiplier=1,
    )

    return RetryExecutor(policy)


@pytest.fixture
def payment_service(
    unit_of_work,
    gateway_factory,
    retry_executor,
):

    return PaymentService(
        unit_of_work=unit_of_work,
        gateway_factory=gateway_factory,
        retry_executor=retry_executor,
    )


@pytest.fixture
def controller(payment_service):

    return PaymentController(
        payment_service
    )


@pytest.fixture
def reconciliation_service(
    unit_of_work,
    gateway_factory,
):

    return ReconciliationService(
        unit_of_work=unit_of_work,
        gateway_factory=gateway_factory,
    )


@pytest.fixture
def outbox_publisher(
    unit_of_work,
    publisher,
):

    return OutboxPublisher(
        unit_of_work=unit_of_work,
        publisher=publisher,
    )


# =========================================================
# DETERMINISTIC SUCCESS GATEWAY
# =========================================================

@pytest.fixture
def successful_gateway():

    result = GatewayPaymentResult(
        status=ProviderResultStatus.SUCCESS,
        provider_transaction_id="TEST-TXN-001",
    )

    return FakePaymentGateway(
        result=result
    )


@pytest.fixture
def successful_controller(
    unit_of_work,
    successful_gateway,
    retry_executor,
):

    gateway_factory = FakeGatewayFactory(
        gateway=successful_gateway
    )

    payment_service = PaymentService(
        unit_of_work=unit_of_work,
        gateway_factory=gateway_factory,
        retry_executor=retry_executor,
    )

    return PaymentController(
        payment_service
    )