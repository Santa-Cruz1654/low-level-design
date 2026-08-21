from typing import Optional

from domain.outbox import OutboxEvent

from .outbox_base import OutboxRepository


class InMemoryOutboxRepository(
    OutboxRepository
):

    def __init__(self):

        self.events: dict[str, OutboxEvent] = {}

    def add(
        self,
        event: OutboxEvent,
    ) -> None:

        self.events[event.event_id] = event

    def get_unpublished(
        self,
    ) -> list[OutboxEvent]:

        return [
            event
            for event in self.events.values()
            if event.published_at is None
        ]

    def mark_published(
        self,
        event_id: str,
    ) -> None:

        event: Optional[
            OutboxEvent
        ] = self.events.get(event_id)

        if event is None:
            return

        from datetime import datetime, timezone

        event.published_at = datetime.now(
            timezone.utc
        )