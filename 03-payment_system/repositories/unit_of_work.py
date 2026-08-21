from abc import ABC, abstractmethod

from .base import PaymentRepository
from .outbox_base import OutboxRepository


class UnitOfWork(ABC):

    payments: PaymentRepository
    outbox: OutboxRepository

    @abstractmethod
    def __enter__(self):
        pass

    @abstractmethod
    def __exit__(
        self,
        exc_type,
        exc_value,
        traceback,
    ):
        pass

    @abstractmethod
    def commit(self) -> None:
        pass

    @abstractmethod
    def rollback(self) -> None:
        pass