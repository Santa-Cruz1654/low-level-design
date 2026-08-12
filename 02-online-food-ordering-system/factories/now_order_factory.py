from typing import List

from factories.order_factory import OrderFactory
from models.user import User
from models.cart import Cart
from models.restaurant import Restaurant
from models.menu_item import MenuItem
from models.order import Order
from models.delivery_order import DeliveryOrder
from models.pickup_order import PickupOrder
from strategies.payment_strategy import PaymentStrategy
from utils.time_utils import TimeUtils


class NowOrderFactory(OrderFactory):
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
        if order_type == "Delivery":
            order = DeliveryOrder()
            order.set_user_address(user.get_address())
        else:
            order = PickupOrder()
            order.set_restaurant_address(restaurant.get_location())

        order.set_user(user)
        order.set_restaurant(restaurant)
        order.set_items(menu_items)
        order.set_payment_strategy(payment_strategy)
        order.set_scheduled(TimeUtils.get_current_time())
        order.set_total(total_cost)
        return order
