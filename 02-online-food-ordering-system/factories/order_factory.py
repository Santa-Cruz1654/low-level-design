"""
OrderFactory
------------
Factory Method interface. Each concrete factory decides *when* the
order happens (now vs. scheduled) and encapsulates the branching
logic for *which* Order subclass to build (Delivery vs. Pickup).
TomatoApp never calls DeliveryOrder()/PickupOrder() directly — it
only ever talks to this interface.
"""

from abc import ABC, abstractmethod
from typing import List

from models.user import User
from models.cart import Cart
from models.restaurant import Restaurant
from models.menu_item import MenuItem
from models.order import Order
from strategies.payment_strategy import PaymentStrategy


class OrderFactory(ABC):
    @abstractmethod
    def create_order(
        self,
        user: User,
        cart: Cart,
        restaurant: Restaurant,
        menu_items: List[MenuItem],
        payment_strategy: PaymentStrategy,
        total_cost: float,
        order_type: str,
    ) -> Order:
        raise NotImplementedError
