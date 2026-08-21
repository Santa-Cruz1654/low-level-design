from domain.outbox import OutboxEvent

from .publisher import EventPublisher


class InMemoryEventPublisher(EventPublisher):

    def __init__(self):
        self.published_events: list[OutboxEvent] = []

    def publish(
        self,
        event: OutboxEvent,
    ) -> None:

        print(
            f"[Publisher] "
            f"Publishing event "
            f"{event.event_type} "
            f"for payment "
            f"{event.aggregate_id}"
        )

        self.published_events.append(event)