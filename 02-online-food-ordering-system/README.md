# Online Food Ordering System (Python)

Python port of the Java LLD project. Package layout mirrors the
original 1:1 so the mapping is easy to follow:

```
OnlineFoodOrderingSystem/
├── main.py                # composition root (was Main.java)
├── tomato_app.py           # Facade (was TomatoApp.java)
├── models/                 # MenuItem, Restaurant, User, Cart, Order, DeliveryOrder, PickupOrder
├── managers/                # RestaurantManager, OrderManager (Singletons)
├── strategies/               # PaymentStrategy + CreditCard / UPI / NetBanking
├── factories/                # OrderFactory + NowOrderFactory / ScheduledOrderFactory
├── services/                 # NotificationService
└── utils/                    # TimeUtils
```

Run it with:

```bash
python3 main.py
```

No third-party dependencies — standard library only.
