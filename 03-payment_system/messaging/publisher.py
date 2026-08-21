from abc import ABC, abstractmethod

from domain.outbox import OutboxEvent


class EventPublisher(ABC):

    @abstractmethod
    def publish(
        self,
        event: OutboxEvent,
    ) -> None:
        pass