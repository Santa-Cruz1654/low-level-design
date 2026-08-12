"""
TomatoApp (Facade)
-------------------
The single entry point the "outside world" (Main, a CLI, a future
REST layer, ...) talks to. It hides RestaurantManager, OrderManager,
Cart, and the factories behind a small, task-oriented API:
search / select / add-to-cart / checkout / pay. Nothing outside this
class needs to know those subsystems exist.
"""

from typing import List, Optional

from models.user import User
from models.restaurant import Restaurant
from models.menu_item import MenuItem
from models.order import Order
from managers.restaurant_manager import RestaurantManager
from managers.order_manager import OrderManager
from strategies.payment_strategy import PaymentStrategy
from factories.order_factory import OrderFactory
from factories.now_order_factory import NowOrderFactory
from factories.scheduled_order_factory import ScheduledOrderFactory
from services.notification_service import NotificationService


class TomatoApp:
    def __init__(self):
        self._initialize_restaurants()

    def _initialize_restaurants(self) -> None:
        restaurant1 = Restaurant("Bikaner", "Delhi")
        restaurant1.add_menu_item(MenuItem("P1", "Chole Bhature", 120))
        restaurant1.add_menu_item(MenuItem("P2", "Samosa", 15))

        restaurant2 = Restaurant("Haldiram", "Kolkata")
        restaurant2.add_menu_item(MenuItem("P1", "Raj Kachori", 80))
        restaurant2.add_menu_item(MenuItem("P2", "Pav Bhaji", 100))
        restaurant2.add_menu_item(MenuItem("P3", "Dhokla", 50))

        restaurant3 = Restaurant("Saravana Bhavan", "Chennai")
        restaurant3.add_menu_item(MenuItem("P1", "Masala Dosa", 90))
        restaurant3.add_menu_item(MenuItem("P2", "Idli Vada", 60))
        restaurant3.add_menu_item(MenuItem("P3", "Filter Coffee", 30))

        restaurant_manager = RestaurantManager.get_instance()
        restaurant_manager.add_restaurant(restaurant1)
        restaurant_manager.add_restaurant(restaurant2)
        restaurant_manager.add_restaurant(restaurant3)

    def search_restaurants(self, location: str) -> List[Restaurant]:
        return RestaurantManager.get_instance().search_by_location(location)

    def select_restaurant(self, user: User, restaurant: Restaurant) -> None:
        user.get_cart().set_restaurant(restaurant)

    def add_to_cart(self, user: User, item_code: str) -> None:
        restaurant = user.get_cart().get_restaurant()
        if restaurant is None:
            print("Please select a restaurant first.")
            return
        for item in restaurant.get_menu():
            if item.get_code() == item_code:
                user.get_cart().add_item(item)
                break

    def checkout_now(
        self, user: User, order_type: str, payment_strategy: PaymentStrategy
    ) -> Optional[Order]:
        return self.checkout(user, order_type, payment_strategy, NowOrderFactory())

    def checkout_scheduled(
        self,
        user: User,
        order_type: str,
        payment_strategy: PaymentStrategy,
        schedule_time: str,
    ) -> Optional[Order]:
        return self.checkout(
            user, order_type, payment_strategy, ScheduledOrderFactory(schedule_time)
        )

    def checkout(
        self,
        user: User,
        order_type: str,
        payment_strategy: PaymentStrategy,
        order_factory: OrderFactory,
    ) -> Optional[Order]:
        if user.get_cart().is_empty():
            return None

        user_cart = user.get_cart()
        ordered_restaurant = user_cart.get_restaurant()
        items_ordered = user_cart.get_items()
        total_cost = user_cart.get_total_cost()

        order = order_factory.create_order(
            user, user_cart, ordered_restaurant, items_ordered,
            payment_strategy, total_cost, order_type,
        )
        OrderManager.get_instance().add_order(order)
        return order

    def pay_for_order(self, user: User, order: Order) -> None:
        is_payment_success = order.process_payment()
        if is_payment_success:
            NotificationService.notify(order)
            user.get_cart().clear()

    def print_user_cart(self, user: User) -> None:
        print("Items in cart:")
        print("------------------------------------")
        for item in user.get_cart().get_items():
            print(f"{item.get_code()} : {item.get_name()} : ₹{item.get_price()}")
        print("------------------------------------")
        print(f"Grand total : ₹{user.get_cart().get_total_cost()}")
