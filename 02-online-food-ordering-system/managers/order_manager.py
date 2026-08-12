"""
OrderManager (Singleton)
--------------------------
Owns the single, app-wide list of placed orders.
"""

from typing import List, Optional

from models.order import Order


class OrderManager:
    _instance: Optional["OrderManager"] = None

    def __init__(self):
        if OrderManager._instance is not None:
            raise RuntimeError("OrderManager is a singleton — use get_instance().")
        self._orders: List[Order] = []

    @classmethod
    def get_instance(cls) -> "OrderManager":
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def add_order(self, order: Order) -> None:
        self._orders.append(order)

    def list_orders(self) -> None:
        print("\n--- All Orders ---")
        for order in self._orders:
            print(
                f"{order.get_type()} order for {order.get_user().get_name()} "
                f"| Total: ₹{order.get_total()} | At: {order.get_scheduled()}"
            )
