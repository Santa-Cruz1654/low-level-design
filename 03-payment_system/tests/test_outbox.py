from application.commands import ProcessPaymentCommand
from domain.enums import GatewayType


def test_payment_creates_outbox_event(
    controller,
    unit_of_work,
):

    command = ProcessPaymentCommand(
        sender="Aditya",
        receiver="Shubham",
        amount=1000.0,
        currency="INR",
        idempotency_key="OUTBOX-001",
        gateway_type=GatewayType.PAYTM,
    )

    payment = controller.handle_payment(
        command
    )

    events = (
        unit_of_work.outbox.get_unpublished()
    )

    assert len(events) >= 1

    assert any(
        event.aggregate_id == payment.payment_id
        for event in events
    )


def test_outbox_event_is_published(
    controller,
    unit_of_work,
    outbox_publisher,
    publisher,
):

    command = ProcessPaymentCommand(
        sender="Aditya",
        receiver="Shubham",
        amount=1000.0,
        currency="INR",
        idempotency_key="OUTBOX-002",
        gateway_type=GatewayType.PAYTM,
    )

    controller.handle_payment(command)

    outbox_publisher.publish_pending_events()

    assert len(
        publisher.published_events
    ) >= 1

    unpublished = (
        unit_of_work.outbox.get_unpublished()
    )

    assert len(unpublished) == 0