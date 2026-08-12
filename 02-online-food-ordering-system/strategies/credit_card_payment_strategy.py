from strategies.payment_strategy import PaymentStrategy


class CreditCardPaymentStrategy(PaymentStrategy):
    def __init__(self, card_number: str):
        self._card_number = card_number

    def pay(self, amount: float) -> None:
        print(f"Paid ₹{amount} using Credit Card ({self._card_number})")
