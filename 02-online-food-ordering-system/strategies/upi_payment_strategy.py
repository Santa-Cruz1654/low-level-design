from strategies.payment_strategy import PaymentStrategy


class UpiPaymentStrategy(PaymentStrategy):
    def __init__(self, mobile: str):
        self._mobile = mobile

    def pay(self, amount: float) -> None:
        print(f"Paid ₹{amount} using UPI ({self._mobile})")
