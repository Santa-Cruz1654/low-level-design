"""
Cart
----
Belongs to a User. Holds the restaurant currently being ordered from
and the items picked from that restaurant's menu.
"""

import sys
from typing import List, Optional

from models.menu_item import MenuItem
from models.restaurant import Restaurant


class Cart:
    def __init__(self):
        self._restaurant: Optional[Restaurant] = None
        self._items: List[MenuItem] = []

    def add_item(self, item: MenuItem) -> None:
        if self._restaurant is None:
            print("Cart: Set a restaurant before adding items.", file=sys.stderr)
            return
        self._items.append(item)

    def get_total_cost(self) -> float:
        return sum(item.get_price() for item in self._items)

    def is_empty(self) -> bool:
        return self._restaurant is None or len(self._items) == 0

    def clear(self) -> None:
        self._items.clear()
        self._restaurant = None

    def set_restaurant(self, restaurant: Restaurant) -> None:
        self._restaurant = restaurant

    def get_restaurant(self) -> Optional[Restaurant]:
        return self._restaurant

    def get_items(self) -> List[MenuItem]:
        return self._items
