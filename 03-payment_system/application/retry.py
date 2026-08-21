import time
from typing import Callable, TypeVar

from application.retry_policy import RetryPolicy


T = TypeVar("T")


class RetryExecutor:
    """
    Executes an operation with retry support.

    Only exceptions listed in retryable_exceptions
    will trigger a retry.
    """

    def __init__(
        self,
        policy: RetryPolicy,
        retryable_exceptions=(
            TimeoutError,
            ConnectionError,
        ),
    ):
        self.policy = policy
        self.retryable_exceptions = (
            retryable_exceptions
        )

    def execute(
        self,
        operation: Callable[[], T],
    ) -> T:

        last_exception = None

        for attempt in range(
            1,
            self.policy.max_attempts + 1,
        ):

            try:
                return operation()

            except self.retryable_exceptions as exc:

                last_exception = exc

                if (
                    attempt
                    >= self.policy.max_attempts
                ):
                    raise

                delay = self._calculate_delay(
                    attempt
                )

                if delay > 0:
                    time.sleep(delay)

            except Exception:
                # Non-retryable exception.
                # Do not hide it and do not retry it.
                raise

        # This should never normally be reached.
        if last_exception is not None:
            raise last_exception

        raise RuntimeError(
            "Retry execution failed unexpectedly."
        )

    def _calculate_delay(
        self,
        attempt: int,
    ) -> float:

        delay = (
            self.policy.initial_delay_seconds
            * (
                self.policy.backoff_multiplier
                ** (attempt - 1)
            )
        )

        return min(
            delay,
            self.policy.max_delay_seconds,
        )