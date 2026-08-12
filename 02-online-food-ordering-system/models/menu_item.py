"""
MenuItem
--------
Simple data-holder (POJO/DTO equivalent) representing a single dish
that a restaurant sells.
"""


class MenuItem:
    def __init__(self, code: str, name: str, price: int):
        self._code = code
        self._name = name
        self._price = price

    # --- getters / setters (kept to mirror the original Java API) ---
    def get_code(self) -> str:
        return self._code

    def set_code(self, code: str) -> None:
        self._code = code

    def get_name(self) -> str:
        return self._name

    def set_name(self, name: str) -> None:
        self._name = name

    def get_price(self) -> int:
        return self._price

    def set_price(self, price: int) -> None:
        self._price = price

    def __repr__(self) -> str:
        return f"MenuItem({self._code}, {self._name}, ₹{self._price})"
