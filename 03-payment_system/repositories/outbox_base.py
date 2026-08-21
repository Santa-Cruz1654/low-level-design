from abc import ABC, abstractmethod

from domain.outbox import OutboxEvent


class OutboxRepository(ABC):

    @abstractmethod
    def add(self, event: OutboxEvent) -> None:
        pass

    @abstractmethod
    def get_unpublished(self) -> list[OutboxEvent]:
        pass

    @abstractmethod
    def mark_published(self, event_id: str) -> None:
        pass