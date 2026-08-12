"""
Composition root — the only place that wires the app together and
kicks off the "happy path" simulation described in the original
Main.java.
"""

from models.user import User
from strategies.upi_payment_strategy import UpiPaymentStrategy
from tomato_app import TomatoApp


def main() -> None:
    # Create TomatoApp object
    tomato = TomatoApp()

    # Simulate a user coming in (Happy Flow)
    user = User(101, "Aditya", "Delhi")
    print(f"User: {user.get_name()} is active.")

    # User searches for restaurants by location
    restaurant_list = tomato.search_restaurants("Delhi")
    if not restaurant_list:
        print("No restaurants found!")
        return

    print("Found Restaurants:")
    for restaurant in restaurant_list:
        print(f" - {restaurant.get_name()}")

    # User selects a restaurant
    tomato.select_restaurant(user, restaurant_list[0])
    print(f"Selected restaurant: {restaurant_list[0].get_name()}")

    # User adds items to the cart
    tomato.add_to_cart(user, "P1")
    tomato.add_to_cart(user, "P2")
    tomato.print_user_cart(user)

    # User checks out the cart
    order = tomato.checkout_now(user, "Delivery", UpiPaymentStrategy("1234567890"))

    # User pays for the cart. If payment is successful, notification is sent.
    tomato.pay_for_order(user, order)


if __name__ == "__main__":
    main()
