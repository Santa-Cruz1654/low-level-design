"""
PaymentStrategy
----------------
The Strategy interface. Every concrete payment mode (credit card,
UPI, net banking, ...) implements `pay`. Order holds a reference to
one PaymentStrategy and delegates to it at payment time -- this is
what lets you swap payment modes without touching Order at all
(Open/Closed Principle).
"""

from abc import ABC, abstractmethod


class PaymentStrategy(ABC):
    @abstractmethod
    def pay(self, amount: float) -> None:
        raise NotImplementedError
