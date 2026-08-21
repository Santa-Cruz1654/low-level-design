from .unit_of_work import UnitOfWork
from .in_memory import InMemoryPaymentRepository
from .outbox_in_memory import InMemoryOutboxRepository


class InMemoryUnitOfWork(UnitOfWork):

    def __init__(
        self,
        payments=None,
        outbox=None,
    ):

        self.payments = (
            payments
            or InMemoryPaymentRepository()
        )

        self.outbox = (
            outbox
            or InMemoryOutboxRepository()
        )

        self._committed = False

    def __enter__(self):

        self._committed = False

        return self

    def __exit__(
        self,
        exc_type,
        exc_value,
        traceback,
    ):

        if exc_type is not None:
            self.rollback()

        return False

    def commit(self) -> None:

        self._committed = True

    def rollback(self) -> None:

        self._committed = False