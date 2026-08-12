"""
Restaurant
----------
Holds identity, location and the menu (composition of MenuItem).
"""

from typing import List
from itertools import count

from models.menu_item import MenuItem


class Restaurant:
    # class-level counter -> mirrors Java's `static int nextRestaurantId`
    _id_counter = count(1)

    def __init__(self, name: str, location: str):
        self._restaurant_id = next(Restaurant._id_counter)
        self._name = name
        self._location = location
        self._menu: List[MenuItem] = []

    def get_id(self) -> int:
        return self._restaurant_id

    def get_name(self) -> str:
        return self._name

    def set_name(self, name: str) -> None:
        self._name = name

    def get_location(self) -> str:
        return self._location

    def set_location(self, location: str) -> None:
        self._location = location

    def add_menu_item(self, item: MenuItem) -> None:
        self._menu.append(item)

    def get_menu(self) -> List[MenuItem]:
        return self._menu

    def __repr__(self) -> str:
        return f"Restaurant(#{self._restaurant_id}, {self._name}, {self._location})"
