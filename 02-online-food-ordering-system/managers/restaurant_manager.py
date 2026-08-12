"""
RestaurantManager (Singleton)
------------------------------
Owns the single, app-wide list of restaurants. `get_instance()` is
the only public way to obtain it, so no matter where in the app you
call it from, everyone shares the same list.
"""

from typing import List, Optional

from models.restaurant import Restaurant


class RestaurantManager:
    _instance: Optional["RestaurantManager"] = None

    def __init__(self):
        if RestaurantManager._instance is not None:
            raise RuntimeError("RestaurantManager is a singleton — use get_instance().")
        self._restaurants: List[Restaurant] = []

    @classmethod
    def get_instance(cls) -> "RestaurantManager":
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def add_restaurant(self, restaurant: Restaurant) -> None:
        self._restaurants.append(restaurant)

    def search_by_location(self, location: str) -> List[Restaurant]:
        location = location.lower()
        return [r for r in self._restaurants if r.get_location().lower() == location]
