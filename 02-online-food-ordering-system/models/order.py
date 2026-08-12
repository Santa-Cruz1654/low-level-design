"""
Order (abstract)
-----------------
Base class for DeliveryOrder / PickupOrder. Holds everything common
to any order (user, restaurant, items, payment strategy, total) and
delegates the actual payment call to whatever PaymentStrategy was
attached (Strategy pattern in action).

`get_type()` is the one piece each subclass must supply -- this is
what factories.OrderFactory.create_order() uses internally to decide
which concrete subclass to instantiate.
"""

from abc import ABC, abstractmethod
from itertools import count
from typing import List, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from models.user import User
    from models.restaurant import Restaurant
    from models.menu_item import MenuItem
    from strategies.payment_strategy import PaymentStrategy


class Order(ABC):
    _id_counter = count(1)

    def __init__(self):
        self._order_id = next(Order._id_counter)
        self.user: Optional["User"] = None
        self.restaurant: Optional["Restaurant"] = None
        self.items: List["MenuItem"] = []
        self.payment_strategy: Optional["PaymentStrategy"] = None
        self.total: float = 0.0
        self.scheduled: str = ""

    def process_payment(self) -> bool:
        if self.payment_strategy is not None:
            self.payment_strategy.pay(self.total)
            return True
        print("Please choose a payment mode first")
        return False

    @abstractmethod
    def get_type(self) -> str:
        raise NotImplementedError

    # --- getters / setters ---
    def get_order_id(self) -> int:
        return self._order_id

    def set_user(self, user: "User") -> None:
        self.user = user

    def get_user(self) -> "User":
        return self.user

    def set_restaurant(self, restaurant: "Restaurant") -> None:
        self.restaurant = restaurant

    def get_restaurant(self) -> "Restaurant":
        return self.restaurant

    def set_items(self, items: List["MenuItem"]) -> None:
        self.items = items
        self.total = sum(i.get_price() for i in items)

    def get_items(self) -> List["MenuItem"]:
        return self.items

    def set_payment_strategy(self, strategy: "PaymentStrategy") -> None:
        self.payment_strategy = strategy

    def set_scheduled(self, scheduled: str) -> None:
        self.scheduled = scheduled

    def get_scheduled(self) -> str:
        return self.scheduled

    def get_total(self) -> float:
        return self.total

    def set_total(self, total: float) -> None:
        self.total = total
