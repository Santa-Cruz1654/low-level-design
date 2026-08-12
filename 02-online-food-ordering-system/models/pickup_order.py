from models.order import Order


class PickupOrder(Order):
    def __init__(self):
        super().__init__()
        self._restaurant_address = ""

    def get_type(self) -> str:
        return "Pickup"

    def set_restaurant_address(self, address: str) -> None:
        self._restaurant_address = address

    def get_restaurant_address(self) -> str:
        return self._restaurant_address
