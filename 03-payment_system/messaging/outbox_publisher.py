from .publisher import EventPublisher


class OutboxPublisher:

    def __init__(
        self,
        unit_of_work,
        publisher: EventPublisher,
    ):
        self.unit_of_work = unit_of_work
        self.publisher = publisher

    def publish_pending_events(self) -> None:

        with self.unit_of_work as uow:

            events = (
                uow.outbox.get_unpublished()
            )

        for event in events:

            try:

                self.publisher.publish(event)

                with self.unit_of_work as uow:

                    uow.outbox.mark_published(
                        event.event_id
                    )

                    uow.commit()

            except Exception as exc:

                print(
                    f"[OutboxPublisher] "
                    f"Failed to publish "
                    f"{event.event_id}: "
                    f"{exc}"
                )