import pytest

from domain.enums import PaymentStatus
from domain.state_machine import PaymentStateMachine


def test_created_to_processing():

    PaymentStateMachine.transition(
        PaymentStatus.CREATED,
        PaymentStatus.PROCESSING,
    )


def test_processing_to_success():

    PaymentStateMachine.transition(
        PaymentStatus.PROCESSING,
        PaymentStatus.SUCCESS,
    )


def test_processing_to_failed():

    PaymentStateMachine.transition(
        PaymentStatus.PROCESSING,
        PaymentStatus.FAILED,
    )


def test_processing_to_unknown():

    PaymentStateMachine.transition(
        PaymentStatus.PROCESSING,
        PaymentStatus.UNKNOWN,
    )


def test_unknown_to_success():

    PaymentStateMachine.transition(
        PaymentStatus.UNKNOWN,
        PaymentStatus.SUCCESS,
    )


def test_unknown_to_failed():

    PaymentStateMachine.transition(
        PaymentStatus.UNKNOWN,
        PaymentStatus.FAILED,
    )


def test_success_to_processing_is_rejected():

    with pytest.raises(Exception):

        PaymentStateMachine.transition(
            PaymentStatus.SUCCESS,
            PaymentStatus.PROCESSING,
        )


def test_failed_to_processing_is_rejected():

    with pytest.raises(Exception):

        PaymentStateMachine.transition(
            PaymentStatus.FAILED,
            PaymentStatus.PROCESSING,
        )


def test_success_to_failed_is_rejected():

    with pytest.raises(Exception):

        PaymentStateMachine.transition(
            PaymentStatus.SUCCESS,
            PaymentStatus.FAILED,
        )


def test_failed_to_success_is_rejected():

    with pytest.raises(Exception):

        PaymentStateMachine.transition(
            PaymentStatus.FAILED,
            PaymentStatus.SUCCESS,
        )