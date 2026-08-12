"""
User
----
Each user owns exactly one Cart (composition — the Cart's lifecycle
is tied to the User's).
"""

from models.cart import Cart


class User:
    def __init__(self, user_id: int, name: str, address: str):
        self._user_id = user_id
        self._name = name
        self._address = address
        self._cart = Cart()

    def get_id(self) -> int:
        return self._user_id

    def get_name(self) -> str:
        return self._name

    def set_name(self, name: str) -> None:
        self._name = name

    def get_address(self) -> str:
        return self._address

    def set_address(self, address: str) -> None:
        self._address = address

    def get_cart(self) -> Cart:
        return self._cart
