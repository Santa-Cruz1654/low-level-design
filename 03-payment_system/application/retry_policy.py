from dataclasses import dataclass


@dataclass(frozen=True)
class RetryPolicy:

    max_attempts: int = 3

    initial_delay_seconds: float = 1.0

    max_delay_seconds: float = 10.0

    backoff_multiplier: float = 2.0

    def get_delay(
        self,
        attempt: int,
    ) -> float:

        delay = (
            self.initial_delay_seconds
            * (
                self.backoff_multiplier
                ** (attempt - 1)
            )
        )

        return min(
            delay,
            self.max_delay_seconds,
        )