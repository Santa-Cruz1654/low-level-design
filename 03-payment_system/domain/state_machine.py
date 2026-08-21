from .enums import PaymentStatus
from .exceptions import InvalidPaymentStateException


class PaymentStateMachine:

    ALLOWED_TRANSITIONS = {
        PaymentStatus.CREATED: {
            PaymentStatus.PROCESSING,
        },

        PaymentStatus.PROCESSING: {
            PaymentStatus.SUCCESS,
            PaymentStatus.FAILED,
            PaymentStatus.UNKNOWN,
        },

        PaymentStatus.UNKNOWN: {
            PaymentStatus.SUCCESS,
            PaymentStatus.FAILED,
        },

        PaymentStatus.SUCCESS: set(),

        PaymentStatus.FAILED: set(),
    }

    @classmethod
    def transition(
        cls,
        current: PaymentStatus,
        new: PaymentStatus,
    ) -> PaymentStatus:

        allowed_states = cls.ALLOWED_TRANSITIONS.get(
            current,
            set(),
        )

        if new not in allowed_states:
            raise InvalidPaymentStateException(
                f"Invalid payment transition: "
                f"{current.value} -> {new.value}"
            )

        return new