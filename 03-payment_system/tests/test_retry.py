import pytest

from application.retry import RetryExecutor
from application.retry_policy import RetryPolicy


# ---------------------------------------------------------
# RetryExecutor tests
# ---------------------------------------------------------

def test_retry_eventually_succeeds():

    attempts = []

    policy = RetryPolicy(
        max_attempts=3,
        initial_delay_seconds=0,
        max_delay_seconds=0,
        backoff_multiplier=1,
    )

    executor = RetryExecutor(policy)

    def flaky_operation():

        attempts.append(1)

        if len(attempts) < 3:
            raise TimeoutError(
                "Temporary timeout"
            )

        return "SUCCESS"

    result = executor.execute(
        flaky_operation
    )

    assert result == "SUCCESS"
    assert len(attempts) == 3


def test_retry_fails_after_max_attempts():

    attempts = []

    policy = RetryPolicy(
        max_attempts=3,
        initial_delay_seconds=0,
        max_delay_seconds=0,
        backoff_multiplier=1,
    )

    executor = RetryExecutor(policy)

    def always_fails():

        attempts.append(1)

        raise TimeoutError(
            "Provider unavailable"
        )

    with pytest.raises(TimeoutError):
        executor.execute(
            always_fails
        )

    assert len(attempts) == 3