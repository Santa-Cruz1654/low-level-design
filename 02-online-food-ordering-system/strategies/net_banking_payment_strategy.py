"""
Your UML diagram shows a third concrete strategy (NetBanking) next to
CreditCard and UPI, even though it wasn't in the Java source you pasted.
Added here so the diagram and the code match 1:1 -- remove it if you
don't need it.
"""

from strategies.payment_strategy import PaymentStrategy


class NetBankingPaymentStrategy(PaymentStrategy):
    def __init__(self, bank_name: str):
        self._bank_name = bank_name

    def pay(self, amount: float) -> None:
        print(f"Paid ₹{amount} using Net Banking ({self._bank_name})")
