from models.order import Order


class DeliveryOrder(Order):
    def __init__(self):
        super().__init__()
        self._user_address = ""

    def get_type(self) -> str:
        return "Delivery"

    def set_user_address(self, address: str) -> None:
        self._user_address = address

    def get_user_address(self) -> str:
        return self._user_address
