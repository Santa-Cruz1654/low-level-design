# Online Food Ordering System — Full LLD Walkthrough

**A block-by-block guide to the code, the theory behind each decision, and how to reuse the same thinking in other LLD problems.**

---

## How to use this document

Every section below covers one file. Each section has four parts:

1. **What this class is responsible for** — one sentence, because if you can't say it in one sentence, the class is probably doing too much.
2. **The code, in blocks** — the actual code, split into logical chunks.
3. **Line-by-block explanation** — what each chunk does and *why* it's written that way.
4. **Theory & how to reuse this** — the transferable idea, stripped of this specific problem, so you can recognize it in the next LLD question you get asked.

Read it in the order given — models first, then the things that manage models, then the things that vary independently (strategies, factories), then the two classes that tie it all together (`TomatoApp`, `main.py`). That's also the order you should *design* a system in: nouns before verbs, verbs before orchestration.

---

## 0. The big picture before you look at any code

Every LLD problem — food ordering, parking lot, elevator, splitwise, whatever — decomposes into the same four questions:

| Question | Answered by | In this project |
|---|---|---|
| What are the **things** in this domain, and what do they know about themselves? | Models | `MenuItem`, `Restaurant`, `User`, `Cart`, `Order` |
| What **varies independently** and needs to be swapped without touching everything else? | Strategy pattern | `PaymentStrategy` and its implementations |
| How do I **construct** something whose exact shape depends on a runtime condition? | Factory pattern | `OrderFactory` and its implementations |
| Where does the **global, shared state** live, and how do I make sure there's only one copy of it? | Singleton pattern | `RestaurantManager`, `OrderManager` |
| How does the **outside world** talk to this system without knowing about any of the above? | Facade pattern | `TomatoApp` |

Keep that table in your head. Almost every LLD interview question is really "which of these five things does this new requirement touch, and how do I add it without breaking the others?"

---

## 1. `models/menu_item.py` — the smallest building block

**Responsibility:** hold the data for one dish. Nothing else.

```python
class MenuItem:
    def __init__(self, code: str, name: str, price: int):
        self._code = code
        self._name = name
        self._price = price

    def get_code(self) -> str:
        return self._code

    def set_code(self, code: str) -> None:
        self._code = code

    def get_name(self) -> str:
        return self._name
    ...
    def get_price(self) -> int:
        return self._price

    def set_price(self, price: int) -> None:
        self._price = price
```

**Block-by-block:**

- `__init__` — takes three plain values and stores them with a leading underscore (`self._code`). The underscore is Python's convention for "treat this as private"; Python doesn't enforce access control the way Java's `private` keyword does, so this is a social contract, not a technical wall. Anyone *can* write `item._price = -50` from outside the class — they just shouldn't, and the underscore signals that.
- The getter/setter pairs (`get_price`/`set_price` etc.) exist purely to mirror the original Java's JavaBean-style API. In idiomatic Python you'd normally replace this whole pattern with `@property`, which I'll show you at the end of this section — but I kept the Java shape here on purpose, because your source diagram uses this style and you may want a 1:1 mapping while learning.

**Theory — encapsulation, and why getters/setters exist at all:**

The reason you don't just make `code`, `name`, `price` public attributes is **encapsulation**: the class controls how its own state can be read and changed. Right now the setters do nothing but assign — but the whole point of routing every read/write through a method is that *later*, if you decide `price` can never go negative, you change it in exactly one place:

```python
def set_price(self, price: int) -> None:
    if price < 0:
        raise ValueError("price cannot be negative")
    self._price = price
```

Every caller everywhere in the codebase is now protected, because none of them ever touched `self._price` directly. If `price` had been a public attribute, that validation would either not exist, or you'd have to hunt down every assignment site in the codebase and add the check by hand.

**The idiomatic Python version**, for when you're not deliberately mirroring Java:

```python
class MenuItem:
    def __init__(self, code: str, name: str, price: int):
        self._code = code
        self._name = name
        self._price = price

    @property
    def price(self) -> int:
        return self._price

    @price.setter
    def price(self, value: int) -> None:
        if value < 0:
            raise ValueError("price cannot be negative")
        self._price = value
```

Callers write `item.price` and `item.price = 90` — reads like a plain attribute, but it's still a method underneath, so you get the same validation hook. This is the Pythonic answer to "how do I do encapsulation without Java-style boilerplate." Worth knowing both, because interviewers sometimes explicitly ask for the Java-style version to test if you understand *why* encapsulation exists independent of syntax.

**How to reuse this idea elsewhere:** any LLD problem has at least one "dumb data" class like this — `Book` in a library system, `Seat` in a booking system, `Product` in an e-commerce system. Recognize it fast, keep it dumb (no business logic inside), and move on. The interesting design decisions live one level up, not here.


---

## 2. `models/restaurant.py` — identity, composition, and a counter idiom

**Responsibility:** represent one restaurant — who it is, where it is, and what it sells.

```python
from itertools import count

class Restaurant:
    _id_counter = count(1)

    def __init__(self, name: str, location: str):
        self._restaurant_id = next(Restaurant._id_counter)
        self._name = name
        self._location = location
        self._menu: List[MenuItem] = []
```

**Block-by-block:**

- `_id_counter = count(1)` is a **class attribute** — it belongs to the `Restaurant` class itself, not to any one instance, so all instances share it. `itertools.count(1)` produces an infinite lazy sequence `1, 2, 3, ...`. This replaces Java's `private static int nextRestaurantId; restaurantId = ++nextRestaurantId;` — same idea (a shared counter that survives across every object creation), just expressed as an iterator instead of a manually-incremented int.
- `next(Restaurant._id_counter)` pulls the next value out of that shared sequence *once*, at construction time, and stores it on `self._restaurant_id` — now it's an **instance attribute**, unique to this one restaurant.
- `self._menu: List[MenuItem] = []` — every restaurant gets its *own* empty list at construction. This matters more than it looks: if you'd written `_menu: List[MenuItem] = []` as a *class* attribute (outside `__init__`), every single `Restaurant` instance would share the exact same list object, and adding a menu item to one restaurant would silently add it to all of them. This is one of the most common real Python bugs — mutable default/class-level containers. Always initialize mutable state (lists, dicts, sets) inside `__init__`, never as a bare class attribute.

```python
    def add_menu_item(self, item: MenuItem) -> None:
        self._menu.append(item)

    def get_menu(self) -> List[MenuItem]:
        return self._menu
```

- `add_menu_item` is the only way to grow the menu from outside — again, encapsulation: nobody appends to `restaurant._menu` directly, they call the method, which is the hook point if you ever want to add validation (e.g., "no duplicate item codes").
- `get_menu` returns the actual internal list, not a copy. That's a deliberate simplification here (the caller genuinely just wants to read it), but it's worth knowing the trade-off: whoever calls `get_menu()` gets a live reference and *could* mutate it directly, bypassing `add_menu_item`. If that mattered, you'd return `list(self._menu)` (a shallow copy) instead. In a portfolio writeup, mentioning "I return the live list here for simplicity, but a stricter version would return a copy to prevent external mutation" shows you understand the trade-off rather than having missed it.

**Theory — identity vs. equality, and the class-attribute-as-shared-counter idiom:**

`restaurant_id` exists because *two restaurants can have the same name* (two different "Haldiram" branches), but they must never be confused with each other in code — the ID is what makes each one uniquely identifiable regardless of its other attributes changing over time. This is the general LLD idea of an **identity field** (sometimes literally called an "entity" in DDD terminology, as opposed to a "value object" like `MenuItem`, which has no identity of its own and is only ever meaningful in the context of the restaurant that sells it).

The `itertools.count()` pattern is worth memorizing — it comes up constantly: order IDs, booking IDs, ticket numbers, transaction IDs. Any time a spec says "auto-incrementing ID," reach for this instead of a manually incremented `self._counter += 1` on some manager class, because it keeps the ID-generation logic inside the entity itself rather than scattered across whoever happens to be creating instances.

**How to reuse this elsewhere:** any "thing with an auto-generated ID" — `Book.isbn_internal_id`, `Ticket.ticket_id`, `Account.account_number` — follows this exact shape. And the "list must be created in `__init__`, never as a class attribute" rule applies to every has-many relationship you'll ever model (a `Library` and its `books`, a `Playlist` and its `songs`, a `Team` and its `members`).


---

## 3. `models/cart.py` — a stateful "working area" object

**Responsibility:** hold what one user is currently in the process of ordering, before it becomes a real `Order`.

```python
class Cart:
    def __init__(self):
        self._restaurant: Optional[Restaurant] = None
        self._items: List[MenuItem] = []

    def add_item(self, item: MenuItem) -> None:
        if self._restaurant is None:
            print("Cart: Set a restaurant before adding items.", file=sys.stderr)
            return
        self._items.append(item)
```

**Block-by-block:**

- `self._restaurant: Optional[Restaurant] = None` — a cart can exist with *no* restaurant chosen yet (right after a `User` is created). The type hint `Optional[Restaurant]` documents that this field can legitimately be `None`, which matters because every method that touches `_restaurant` has to handle that case.
- `add_item` is a **guard clause**: check the precondition first, and bail out early (with a message to `stderr`, not `stdout`, because this is diagnostic/error output, not part of the program's normal output) if it isn't met. This enforces a business rule — *you cannot add food from a restaurant you haven't selected* — inside the one class responsible for the cart's own consistency, rather than trusting every caller to check this themselves before calling `add_item`.

```python
    def get_total_cost(self) -> float:
        return sum(item.get_price() for item in self._items)

    def is_empty(self) -> bool:
        return self._restaurant is None or len(self._items) == 0
```

- `get_total_cost` uses a **generator expression** inside `sum()` — `sum(item.get_price() for item in self._items)` — instead of a manual loop with an accumulator variable. This is the idiomatic Python replacement for:
  ```python
  total = 0
  for item in self._items:
      total += item.get_price()
  return total
  ```
  Both do exactly the same thing; the generator version is preferred in Python because it's shorter, has no mutable loop variable to accidentally misuse, and reads as "the sum of each item's price" rather than "build up a total by repeatedly adding to it." You'll use this pattern constantly — anywhere you're aggregating a list into a single number (totals, counts, averages).
- `is_empty` — note the `or`. A cart with a restaurant selected but zero items is empty. A cart with *no restaurant* is also considered empty (there's nothing meaningful to check out). Two different conditions, either one makes the cart "empty" — this is exactly what `or` is for.

```python
    def clear(self) -> None:
        self._items.clear()
        self._restaurant = None

    def set_restaurant(self, restaurant: Restaurant) -> None:
        self._restaurant = restaurant
```

- `clear()` resets *both* fields — after checkout succeeds, the cart needs to go back to its brand-new state, ready for the next order. If you only cleared `_items` and left `_restaurant` set, the user's next `add_item` call would silently succeed against stale restaurant context instead of forcing them to pick a restaurant again — a subtle bug that only shows up much later.

**Theory — the "working area" / draft object pattern:**

`Cart` is what's sometimes called a **staging object** or **draft** — it's mutable, temporary, and gets thrown away (or converted into something else) once its job is done. This is a different flavor of object than `MenuItem` (immutable-ish value) or `Restaurant` (long-lived entity). Recognizing which flavor a class is tells you a lot about how to design it: drafts get a `clear()`/reset method and usually a `to_X()` conversion method (here, that conversion happens externally in `TomatoApp.checkout`, which reads the cart's contents to build an `Order`).

**How to reuse this elsewhere:** any LLD problem with a "build up state, then commit it" flow has one of these — a shopping cart (obviously), a form draft, a "current game move being assembled" in a chess LLD, an in-progress booking in a hotel-reservation LLD. The shape is always: mutable container + guard clauses on mutation + a clear/reset + something else reads it to produce the final artifact.


---

## 4. `models/user.py` — composition in action

**Responsibility:** represent a customer, and own their cart.

```python
class User:
    def __init__(self, user_id: int, name: str, address: str):
        self._user_id = user_id
        self._name = name
        self._address = address
        self._cart = Cart()
```

**Block-by-block:**

- Everything here is a straightforward constructor except one line that's doing more work than it looks like: `self._cart = Cart()`. A brand-new `Cart` is created **inside** `User.__init__` — the user doesn't receive a cart from outside, doesn't share one with anyone else, and can't exist without one.

**Theory — composition ("has-a" with ownership), and why it's different from aggregation:**

This is what UML calls **composition**, drawn as the filled/black diamond on your diagram between `User` and `Cart`. The defining property of composition is *lifecycle dependency*: the `Cart` cannot outlive the `User` — when the `User` object is garbage collected, so is its cart, because nothing else in the system holds a reference to it. Contrast this with **aggregation** (the hollow diamond, e.g. `RestaurantManager` *has* `Restaurant`s), where the contained objects have an independent existence — a `Restaurant` doesn't stop existing if `RestaurantManager` disappears, and in principle a `Restaurant` could be looked up or referenced by multiple other objects.

The tell in the code: composition means the container **constructs** the contained object itself, right there in `__init__` (`self._cart = Cart()`). Aggregation means the container **receives** an already-existing object from outside (`RestaurantManager.add_restaurant(self, r: Restaurant)` — the restaurant was built elsewhere and just handed in).

This distinction sounds academic, but it directly answers a question every LLD interview eventually asks: *"if I delete this, what else has to change?"* Delete a `User` → their `Cart` is meaningless and goes with them (composition, no cleanup needed elsewhere). Delete a `Restaurant` → `RestaurantManager`'s list needs to explicitly remove it (aggregation, cleanup is your responsibility).

**How to reuse this elsewhere:** `Order` *has-a* list of `MenuItem`s is aggregation (the items existed on the restaurant's menu before the order, and continue existing after). `Car` *has-a* `Engine` is usually composition (that specific engine instance is built for that specific car). When you're modeling a new domain, ask "does the contained thing get created by its container, or handed to it?" — that answers the composition-vs-aggregation question every time, and it directly determines whether you write `self.thing = Thing()` or `def __init__(self, thing: Thing)`.

*Composition and aggregation are actually the two tightest members of a larger family of six standard UML relationships — association, dependency, and the inheritance/interface relationships (generalization, realization) round it out. Section 16, in Part II below, covers all six side by side with examples from this exact codebase, including the ones this section doesn't touch on (like `Order.user`, which is neither composition nor aggregation — it's plain association).*


---

## 5. `strategies/payment_strategy.py`, and the three concrete strategies — the Strategy pattern

**Responsibility of the interface:** define the one thing every payment method must be able to do, and nothing about how it does it.

```python
from abc import ABC, abstractmethod

class PaymentStrategy(ABC):
    @abstractmethod
    def pay(self, amount: float) -> None:
        raise NotImplementedError
```

**Block-by-block:**

- `ABC` (Abstract Base Class) is Python's mechanism for declaring "this class cannot be instantiated on its own — it only exists to be subclassed." If you try `PaymentStrategy()` directly, Python raises `TypeError: Can't instantiate abstract class PaymentStrategy with abstract method pay`. This is Python's equivalent of a Java `interface` (or an `abstract class` — Python doesn't distinguish the two syntactically the way Java does; `ABC` covers both use cases).
- `@abstractmethod` marks `pay` as a method that **every concrete subclass must override**. If `CreditCardPaymentStrategy` forgot to implement `pay`, it would also fail to instantiate, with the same `TypeError`. This is what makes the interface a *contract*, not just documentation — Python enforces it at instantiation time, not just via a type checker.
- The body `raise NotImplementedError` never actually runs (Python won't let you get far enough to call it on the base class), but it's a defensive convention in case someone calls `super().pay(amount)` from a subclass by mistake.

Now the concrete implementations:

```python
class UpiPaymentStrategy(PaymentStrategy):
    def __init__(self, mobile: str):
        self._mobile = mobile

    def pay(self, amount: float) -> None:
        print(f"Paid ₹{amount} using UPI ({self._mobile})")
```

```python
class CreditCardPaymentStrategy(PaymentStrategy):
    def __init__(self, card_number: str):
        self._card_number = card_number

    def pay(self, amount: float) -> None:
        print(f"Paid ₹{amount} using Credit Card ({self._card_number})")
```

**Block-by-block:**

- Each concrete strategy takes whatever data *it specifically* needs in its own `__init__` (a mobile number for UPI, a card number for credit card) — this data does **not** live on `PaymentStrategy` or on `Order`. `Order` never needs to know a card number exists; it just knows it's holding *some* `PaymentStrategy` and can call `.pay()` on it.
- `pay()` in each subclass does something completely different internally, but from the outside — from `Order`'s point of view — every strategy looks identical: "an object with a `.pay(amount)` method." This is called **polymorphism**: the same method call (`payment_strategy.pay(total)`) produces different behavior depending on which concrete object is actually behind the `payment_strategy` reference at runtime.

**Where the pattern is actually used — this is the part that matters:**

```python
# in models/order.py
def process_payment(self) -> bool:
    if self.payment_strategy is not None:
        self.payment_strategy.pay(self.total)
        return True
    print("Please choose a payment mode first")
    return False
```

`Order.process_payment` has **zero knowledge** of UPI, credit cards, or net banking. It only knows `self.payment_strategy` has a `.pay()` method. This is the entire point of the pattern.

**Theory — Strategy pattern, and the Open/Closed Principle it exists to satisfy:**

The **Strategy pattern** is: *take an algorithm (or behavior) that can vary, extract it into its own family of interchangeable classes behind a common interface, and have the "owning" object hold a reference to one of them instead of hard-coding the behavior itself.*

The concrete reason this matters is the **Open/Closed Principle** (the "O" in SOLID): *a class should be open for extension, but closed for modification.* Watch what happens when your product manager says "we need to support Net Banking":

- **Without Strategy** (the bad version): `Order.process_payment` would contain an `if payment_type == "upi": ... elif payment_type == "credit_card": ...` chain. Adding Net Banking means **opening up and editing `Order`** — a class that already works, that other code already depends on, that you now risk breaking, and that needs to be re-tested.
- **With Strategy** (what you have): Adding Net Banking means writing one new class, `NetBankingPaymentStrategy(PaymentStrategy)`, that implements `pay()`. `Order` is never touched. `Order.process_payment` was true on day one and remains true forever, regardless of how many payment methods get added later.

This is the single most important idea to internalize from this whole project, because it's the most commonly-tested LLD pattern by a wide margin. Any time an interviewer says "how would you support a new payment method / new discount type / new notification channel / new shipping method without modifying existing code," the answer is Strategy.

**A subtlety worth mentioning if asked:** Strategy and simple polymorphism can look identical in code. The distinction is *intent*: Strategy specifically refers to swapping the algorithm at **runtime**, often via composition (an object *holds* a strategy) rather than inheritance (an object *is-a* type of thing). `Order` isn't a `CreditCardOrder` subclass — it *has-a* `payment_strategy` that could be reassigned at any point before payment. That's what makes it Strategy rather than "just polymorphism."

**How to reuse this elsewhere:** any time a spec has the words "different ways of doing X" — sorting strategies, discount/pricing strategies, notification-channel strategies (email vs. SMS vs. push), route-finding strategies, compression strategies — reach for this pattern immediately. The shape is always: one abstract method on an ABC, N concrete implementations, and exactly one "owning" class that holds a reference to whichever one is currently active and calls it without an `if/elif` chain.


---

## 6. `models/order.py`, `delivery_order.py`, `pickup_order.py` — abstract base class + Template-ish inheritance

**Responsibility of `Order`:** hold everything common to *any* order, and force every concrete order type to answer one question (`get_type`) that the base class can't answer on its own.

```python
class Order(ABC):
    _id_counter = count(1)

    def __init__(self):
        self._order_id = next(Order._id_counter)
        self.user: Optional["User"] = None
        self.restaurant: Optional["Restaurant"] = None
        self.items: List["MenuItem"] = []
        self.payment_strategy: Optional["PaymentStrategy"] = None
        self.total: float = 0.0
        self.scheduled: str = ""
```

**Block-by-block:**

- Same `itertools.count` ID idiom you already saw in `Restaurant` — every `Order`, regardless of whether it ends up being a `DeliveryOrder` or `PickupOrder`, gets a globally unique ID from the **same shared counter**, because `_id_counter` lives on `Order` (the base class), and `DeliveryOrder`/`PickupOrder` don't define their own. This matters: if each subclass had its *own* counter, you could end up with a `DeliveryOrder #1` and a `PickupOrder #1` existing simultaneously — ambiguous IDs. Sharing the counter on the base class guarantees every order, of any type, has a globally unique number.
- `self.user`, `self.restaurant`, etc. are declared **without** a leading underscore here (unlike `MenuItem`/`Restaurant`/`Cart`, which used `self._x`). This is a minor inconsistency carried over from the original Java (which used `protected`, meaning "visible to this class and its subclasses, not outside"). `DeliveryOrder` and `PickupOrder` need direct access to these fields since they inherit from `Order`, so leaving off the underscore here is a deliberate (if debatable) choice, not an oversight — worth being able to explain if someone asks "why is this one different?"
- The `TYPE_CHECKING` import block at the top of the file and the string type hints (`Optional["User"]`) exist purely to solve a **circular import** problem: `strategies/payment_strategy.py` doesn't import `models/order.py`, but if `models/order.py` did a normal `from strategies.payment_strategy import PaymentStrategy` at the top of the file just to use it in a type hint, and some other file created an import cycle later, Python would crash at import time. Wrapping the import inside `if TYPE_CHECKING:` means it only happens when a type-checker (like `mypy`) is analyzing the code — never at actual runtime — and the type hints in quotes (`"PaymentStrategy"`) are "forward references" that Python doesn't try to resolve until/unless something actually asks for them. This is a common, real pattern in medium-sized Python codebases; good to recognize rather than being confused by it.

```python
    def process_payment(self) -> bool:
        if self.payment_strategy is not None:
            self.payment_strategy.pay(self.total)
            return True
        print("Please choose a payment mode first")
        return False

    @abstractmethod
    def get_type(self) -> str:
        raise NotImplementedError
```

- `process_payment` is a **concrete method on an abstract class** — this is allowed and common. `Order` is abstract (you can't do `Order()` directly), but it's not *empty*; it implements everything that's genuinely the same across every order type, and only declares abstract the one thing that genuinely differs (`get_type`).

```python
    def set_items(self, items: List["MenuItem"]) -> None:
        self.items = items
        self.total = sum(i.get_price() for i in items)
```

- Note that `set_items` **recomputes `self.total` every time it's called** — you never trust a caller to separately compute and pass in a total; the moment items are set, the total is derived from them, guaranteeing they can never drift out of sync. (There's a redundant `order.set_total(total_cost)` call later in the factories that overwrites this with the same value — harmless here since `total_cost` was itself derived from `cart.get_total_cost()`, but worth flagging: two different code paths compute "the same" total independently, which is a mild code smell. In a stricter version, you'd compute the total in exactly one place and never pass it around as a separate parameter at all.)

Now the two concrete subclasses:

```python
class DeliveryOrder(Order):
    def __init__(self):
        super().__init__()
        self._user_address = ""

    def get_type(self) -> str:
        return "Delivery"
```

```python
class PickupOrder(Order):
    def __init__(self):
        super().__init__()
        self._restaurant_address = ""

    def get_type(self) -> str:
        return "Pickup"
```

**Block-by-block:**

- `super().__init__()` — this must be the **first thing** each subclass's constructor does. It runs `Order.__init__`, which is what actually assigns the shared-counter `_order_id` and sets up all the common fields. Skip this call and you'd have a `DeliveryOrder` with no `order_id`, no `total`, etc. — this is one of the single most common inheritance bugs in any OOP language.
- Each subclass adds exactly **one** field beyond what `Order` already has (`_user_address` for delivery, `_restaurant_address` for pickup) — the minimum extra state needed to answer "where does this order actually go/get picked up from."
- `get_type()` is the abstract method being fulfilled. Notice it returns a hardcoded string, not something computed — this is intentionally the *simplest possible* differentiation between the two subclasses, which is exactly what makes it a clean example of the pattern.

**Theory — abstract classes vs. interfaces, and why `Order` uses one but `PaymentStrategy` conceptually is "more of" an interface:**

Both `Order` and `PaymentStrategy` inherit from `ABC` in this codebase, so syntactically they look the same. But conceptually they're different kinds of abstraction:

- `PaymentStrategy` is a **pure interface** — it has *no* shared state and *no* shared behavior, only a contract (`pay(amount)`). Nothing is inherited except the promise that `.pay()` exists.
- `Order` is an **abstract base class with a template** — it has substantial shared state (`user`, `restaurant`, `items`, `total`...) and shared behavior (`process_payment`), and only asks subclasses to fill in one specific gap (`get_type`). This is closer to the **Template Method pattern** in spirit (a base class defines the skeleton of an operation and lets subclasses override specific steps), though this codebase doesn't take it as far as a "real" Template Method example would (where the base class would define something like `place_order()` that internally calls several overridable steps in a fixed sequence).

The practical rule of thumb: if your abstraction has fields and non-trivial shared logic, it's an abstract base class. If it's *purely* "here's what you must be able to do," it's an interface. Both use the same `ABC` machinery in Python — the distinction is about what you put inside them, not the syntax.

**How to reuse this elsewhere:** `Vehicle` (abstract, shared fields like `speed`/`fuel`) → `Car`/`Motorcycle` (each fills in `max_capacity()` or similar) is the exact same shape. `PaymentMethod` → `Order` here vs. `Shape` (abstract, maybe shares a `describe()` method) → `Circle`/`Rectangle` (each fills in `area()`). Whenever a spec says "there are several kinds of X, and they're mostly the same except for one or two specific behaviors," this is your pattern: shared abstract base with concrete shared logic, plus `@abstractmethod` for the parts that differ.


---

## 7. `managers/restaurant_manager.py` and `managers/order_manager.py` — the Singleton pattern

**Responsibility:** be the single, authoritative, app-wide collection of restaurants (or orders) — there must never be two competing lists.

```python
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
```

**Block-by-block:**

- `_instance: Optional["RestaurantManager"] = None` — a **class attribute** that will eventually hold the one-and-only instance of the class. It starts as `None`, meaning "not created yet."
- `__init__` has a guard: `if RestaurantManager._instance is not None: raise RuntimeError(...)`. This stops someone from bypassing the pattern by calling `RestaurantManager()` directly a second time — the *first* time it's called (from inside `get_instance`), `_instance` is still `None`, so this check passes silently. Any *subsequent* direct call to the constructor raises. This is what actually enforces "only one instance can ever exist," rather than just hoping nobody calls the constructor directly.
- `@classmethod` — this decorator means `get_instance` receives the **class itself** (`cls`, i.e. `RestaurantManager`) as its first argument, rather than a specific instance (`self`). That's necessary here because at the point this method is called, an instance might not exist yet — there's no `self` to receive.
- `get_instance`'s logic: *if nobody's built one yet, build exactly one now, and remember it; otherwise, hand back the one that already exists.* This is called **lazy initialization** — the object isn't created until the first time it's actually needed, not automatically when the program starts. (The alternative, "eager" initialization, would create the instance immediately when the class is defined — sometimes preferred, but lazy is the more common default because it avoids paying construction cost for a singleton the program might never actually use.)

`OrderManager` follows the identical shape:

```python
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
```

Every call anywhere in the codebase — `RestaurantManager.get_instance()` from `TomatoApp._initialize_restaurants`, and separately from `TomatoApp.search_restaurants` — returns the exact same object. You can verify this yourself:

```python
>>> a = RestaurantManager.get_instance()
>>> b = RestaurantManager.get_instance()
>>> a is b
True
```

**Theory — Singleton, what it actually solves, and its well-known downsides:**

The **Singleton pattern** guarantees exactly one instance of a class exists for the lifetime of the program, and provides one global access point to it. It's used when a piece of state genuinely needs to be shared and consistent across the entire application — a configuration object, a connection pool, a logging service, or here, "the list of all restaurants" (there is exactly one such list; it wouldn't make sense for two different parts of the app to have their own separate, possibly-inconsistent copies).

**The downside, and why senior engineers are often wary of Singletons:** a singleton is **global mutable state**, which fights against two things you usually want in well-designed software:

1. **Testability.** If you write a unit test that adds a restaurant to `RestaurantManager`, that restaurant is still there for the *next* test, because it's the same global instance — unless you explicitly reset it between tests. This is exactly the kind of hidden coupling between unrelated tests that causes "it works when I run it alone but fails in the full suite" bugs.
2. **Explicit dependencies.** When `TomatoApp` calls `RestaurantManager.get_instance()` from deep inside a method, that dependency is invisible from the outside — you can't tell just by looking at `TomatoApp.__init__(self)`'s signature that it depends on a restaurant store at all. The alternative — **dependency injection** — would have `TomatoApp.__init__(self, restaurant_store: RestaurantManager)` take the dependency as a constructor parameter. That makes the dependency visible, swappable (you can inject a fake/mock store in tests), and removes the need for the Singleton pattern's enforcement machinery entirely, because the caller now controls how many instances exist.

If asked in an interview "what's the problem with Singleton, and what would you use instead in a larger system," this is the answer: dependency injection of a single shared instance that's constructed once at the composition root (in this project, that would be `main.py`) and passed down to whoever needs it — same "one shared instance" guarantee, without hiding the dependency or making it hard to substitute in tests.

**How to reuse this elsewhere:** any "there is exactly one of this, app-wide" requirement — a `Logger`, a `ConfigManager`, a `DatabaseConnectionPool`, a `CacheManager`. Recognize the requirement, know how to implement the lazy-init version cold, and also be ready to name its trade-off unprompted — that's usually what separates "I memorized the pattern" from "I understand the pattern" in an interview.


---

## 8. `factories/order_factory.py`, `now_order_factory.py`, `scheduled_order_factory.py` — the Factory Method pattern

**Responsibility:** decide *which concrete `Order` subclass* to build and *when it's stamped for*, so nothing else in the codebase has to know `DeliveryOrder`/`PickupOrder` exist at all.

```python
class OrderFactory(ABC):
    @abstractmethod
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
        raise NotImplementedError
```

**Block-by-block:**

- This is the interface — same `ABC` + `@abstractmethod` shape you've now seen three times (`PaymentStrategy`, and implicitly `Order.get_type`). By this point you should be pattern-matching this shape on sight: *ABC with one abstract method = "there's a family of interchangeable implementations coming."*
- The method signature takes **everything** needed to build any kind of order — user, restaurant, items, payment strategy, cost, and a string flag (`order_type`) that says "Delivery" or "Pickup." That flag is the piece of runtime information the factory uses internally to decide which concrete class to instantiate.

```python
class NowOrderFactory(OrderFactory):
    def create_order(self, user, cart, restaurant, menu_items,
                      payment_strategy, total_cost, order_type):
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
```

**Block-by-block:**

- The `if order_type == "Delivery": ... else: ...` branch is the **one and only place in the entire codebase** where `DeliveryOrder()` or `PickupOrder()` get directly instantiated. `TomatoApp` never does this. `main.py` never does this. This is the whole point: construction logic for a family of related types is quarantined inside the factory, instead of being duplicated (or worse, inconsistently implemented) everywhere an order needs to be created.
- After picking the right subclass, the method calls the same sequence of setters regardless of which branch was taken (`set_user`, `set_restaurant`, `set_items`, `set_payment_strategy`, `set_total`) — only `set_scheduled` differs between the two factory *classes* (not between Delivery/Pickup within the same factory).
- `TimeUtils.get_current_time()` — this factory always stamps the current timestamp. That's its entire reason for existing as a *separate* class from `ScheduledOrderFactory`.

```python
class ScheduledOrderFactory(OrderFactory):
    def __init__(self, schedule_time: str):
        self._schedule_time = schedule_time

    def create_order(self, user, cart, restaurant, menu_items,
                      payment_strategy, total_cost, order_type):
        # ...identical branching and setter calls as above...
        order.set_scheduled(self._schedule_time)
        order.set_total(total_cost)
        return order
```

**Block-by-block:**

- The only two differences from `NowOrderFactory`: (1) this factory has a **constructor** that takes and stores a `schedule_time`, and (2) `set_scheduled` uses that stored value instead of calling `TimeUtils.get_current_time()`. Everything else — the Delivery/Pickup branching, all the other setters — is duplicated between the two files.

  *(Worth naming honestly: this duplication is a legitimate refactor opportunity. A cleaner version would pull the shared branching logic into a protected helper method on `OrderFactory` itself — e.g. `_build_base_order(order_type, user, restaurant)` — that both subclasses call, and let each subclass only override the one line that actually differs, `get_timestamp()`. That would be closer to a true **Template Method** pattern layered inside the Factory Method. I kept it as two independent implementations here because that's what the original Java did and it's easier to read while first learning the pattern — but recognizing "this could be DRY'd up with Template Method" is exactly the kind of observation that shows deeper understanding in an interview.)*

**Theory — Factory Method, and why it's not "just an `if` statement wrapped in a function":**

The **Factory Method pattern** is: *define an interface for creating an object, but let subclasses (or, more loosely in Python, interchangeable implementer classes) decide which concrete class to instantiate.* The caller depends only on the abstract `OrderFactory` interface and the abstract `Order` return type — never on `DeliveryOrder`, `PickupOrder`, `NowOrderFactory`, or `ScheduledOrderFactory` by name.

Look at how `TomatoApp.checkout` actually uses this:

```python
def checkout(self, user, order_type, payment_strategy, order_factory: OrderFactory) -> Optional[Order]:
    ...
    order = order_factory.create_order(user, user_cart, ordered_restaurant, items_ordered,
                                        payment_strategy, total_cost, order_type)
    OrderManager.get_instance().add_order(order)
    return order
```

`checkout` takes an `OrderFactory` as a **parameter** — this is what makes it Factory Method rather than just "a function with a switch statement." The *caller* of `checkout` decides which factory to use (`checkout_now` passes a `NowOrderFactory()`, `checkout_scheduled` passes a `ScheduledOrderFactory(time)`), and `checkout` itself never needs to change to support a hypothetical future third option — say, a `RecurringOrderFactory` for a weekly standing order. You'd write that one new factory class, add one new `checkout_recurring` convenience method on `TomatoApp` that constructs and passes it — and `checkout`'s own body is untouched. Same Open/Closed win you saw with Strategy, applied to *construction* instead of *behavior*.

**The distinction between Factory Method and the (very similar-sounding) Abstract Factory pattern**, since interviewers sometimes probe this: Factory Method is about **one product family with one creation method** (here: "give me an `Order`, some way"). Abstract Factory is about **families of related products created together** — e.g., a `UIFactory` that creates a matching `Button` *and* `Checkbox` *and* `ScrollBar` for a specific OS theme, where you always want all three from the same family, never mixed. If your factory only ever hands back one type of thing, it's Factory Method; if it hands back a coordinated *set* of related objects, it's Abstract Factory.

**How to reuse this elsewhere:** any spec with the words "different ways/timings/modes of creating X" — a `DocumentFactory` that produces PDF vs. Word exports, a `NotificationFactory` that decides SMS vs. Email vs. Push based on user preference, a `ShapeFactory` in a drawing app. The signal to watch for: if you catch yourself about to write `if type == "A": return AObject() elif type == "B": return BObject()` *inside a class that has other responsibilities*, that branching almost always deserves to be pulled out into its own factory hierarchy instead.


---

## 9. `services/notification_service.py` and `utils/time_utils.py` — small, single-purpose helpers

**Responsibility of `NotificationService`:** format and "send" (here, print) a receipt for a completed order. Nothing more.

```python
class NotificationService:
    @staticmethod
    def notify(order: Order) -> None:
        print(f"\nNotification: New {order.get_type()} order placed!")
        ...
        for item in order.get_items():
            print(f"   - {item.get_name()} (₹{item.get_price()})")
        ...
```

**Block-by-block:**

- `@staticmethod` — this method doesn't need `self` (an instance) at all; it doesn't read or write any state that belongs to a `NotificationService` object, because there isn't any — the class has no `__init__`, no fields. It's really just a namespace for a function, called as `NotificationService.notify(order)` without ever constructing a `NotificationService()` instance. This is Python's equivalent of Java's `public static void notify(Order order)`.
- The method takes an `Order` and reads everything it needs (`get_type`, `get_user`, `get_restaurant`, `get_items`, `get_total`, `get_scheduled`) through that one object's public interface — `NotificationService` never reaches into `Cart`, `RestaurantManager`, or anything else. It has exactly one job: given a completed order, describe it.

**Theory — why this is its own class instead of a method on `Order` or `TomatoApp`:**

This is the **Single Responsibility Principle** (the "S" in SOLID) in its purest form: *a class should have one, and only one, reason to change.* `Order`'s reason to change would be "the business rules of what an order *is* changed" (e.g., adding a discount field). `NotificationService`'s reason to change is entirely different: "the way we *communicate* about an order changed" (e.g., switching from console output to sending an actual email via SendGrid, or adding SMS as a second channel). Those are two unrelated concerns, changing for two unrelated reasons, on two unrelated schedules — which is exactly the signal that they belong in two separate classes.

A very common LLD mistake is to put `notify()` as a method directly on `Order`, because "the order needs to notify someone" feels intuitive. The problem shows up the moment requirements evolve: now `Order` needs an SMS provider dependency, an email provider dependency, maybe a push-notification SDK — none of which have anything to do with what an order fundamentally *is* (its items, its total, its status). `Order` has become bloated with unrelated concerns. Keeping `NotificationService` separate means `Order` never needs to know delivery mechanisms exist; it just gets *handed to* the notifier by whoever's orchestrating the flow (`TomatoApp.pay_for_order`).

```python
# utils/time_utils.py
class TimeUtils:
    @staticmethod
    def get_current_time() -> str:
        return datetime.now().strftime("%a %b %d %H:%M:%S %Y")
```

**Block-by-block:**

- Same `@staticmethod`-as-namespace shape as `NotificationService`. `datetime.now()` gets the current local date/time; `.strftime(...)` formats it into a string using format codes (`%a` = abbreviated weekday, `%b` = abbreviated month, `%d` = zero-padded day, `%H:%M:%S` = 24-hour time, `%Y` = 4-digit year) — chosen to match the original Java's `DateTimeFormatter.ofPattern("EEE MMM dd HH:mm:ss yyyy")` output format exactly, so the two versions produce visually identical timestamps.

**How to reuse this elsewhere:** any cross-cutting concern that multiple otherwise-unrelated classes need (formatting, logging, notification, ID generation, currency conversion) belongs in its own small utility/service class, called via static methods when it holds no state of its own — not bolted onto whichever domain class happens to need it first.


---

## 10. `tomato_app.py` — the Facade pattern, and where everything gets wired together

**Responsibility:** be the *only* class the outside world talks to. Hide every other class in this project behind a small, task-oriented API.

```python
class TomatoApp:
    def __init__(self):
        self._initialize_restaurants()

    def _initialize_restaurants(self) -> None:
        restaurant1 = Restaurant("Bikaner", "Delhi")
        restaurant1.add_menu_item(MenuItem("P1", "Chole Bhature", 120))
        ...
        restaurant_manager = RestaurantManager.get_instance()
        restaurant_manager.add_restaurant(restaurant1)
        ...
```

**Block-by-block:**

- `__init__` calls a **private helper method** (`_initialize_restaurants`, leading underscore = "internal, don't call this from outside") that seeds three restaurants with their menus. In a real production system this would instead load from a database — the point of isolating it into its own method, rather than inlining it into `__init__`, is that swapping "hardcoded seed data" for "load from DB" later only touches this one method.
- Notice this constructor is where `Restaurant` and `MenuItem` objects actually get built and handed to `RestaurantManager.get_instance().add_restaurant(...)` — this is the "hollow diamond" aggregation relationship from Section 4 in practice: the restaurants are constructed *here*, in `TomatoApp`, and then *given to* the manager, which just stores references to them.

```python
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
```

**Block-by-block:**

- Each of these methods is a **thin pass-through with light orchestration** — `search_restaurants` literally just forwards to `RestaurantManager`. `select_restaurant` reaches two levels deep (`user.get_cart().set_restaurant(...)`) but is still a single, obvious action. `add_to_cart` is the most "does actual work" method here: it looks up the restaurant currently in the user's cart, linear-searches the restaurant's menu for a matching item code, and adds it if found — but even this is only a few lines, because the *real* logic (what does it mean for a cart to be valid, how items get added) lives inside `Cart` itself, not duplicated here.
- This "thin orchestration, delegate the real logic downward" style is the defining trait of a well-written Facade — if you find yourself writing 40 lines of business logic *inside* a facade method instead of calling into the class that actually owns that concern, that's a sign the facade is taking on responsibilities it shouldn't.

```python
    def checkout_now(self, user, order_type, payment_strategy) -> Optional[Order]:
        return self.checkout(user, order_type, payment_strategy, NowOrderFactory())

    def checkout_scheduled(self, user, order_type, payment_strategy, schedule_time) -> Optional[Order]:
        return self.checkout(user, order_type, payment_strategy, ScheduledOrderFactory(schedule_time))

    def checkout(self, user, order_type, payment_strategy, order_factory: OrderFactory) -> Optional[Order]:
        if user.get_cart().is_empty():
            return None
        ...
        order = order_factory.create_order(...)
        OrderManager.get_instance().add_order(order)
        return order
```

**Block-by-block:**

- `checkout_now` and `checkout_scheduled` are **convenience wrappers**: they exist purely so the caller (`main.py`, or anyone else) never has to know `NowOrderFactory`/`ScheduledOrderFactory` exist by name — you just call `tomato.checkout_now(...)` and the Facade quietly picks the right factory internally. This is Facade hiding Factory Method — two patterns stacked, which is completely normal in real systems.
- `checkout` itself is the one that actually implements Section 8's Factory Method usage: it takes an `OrderFactory` parameter, calls `.create_order(...)` on it without caring which concrete factory it received, then registers the result with `OrderManager` (Section 7's Singleton, called by its access point, not passed in — see the earlier note on why that's a trade-off).
- The early-return guard `if user.get_cart().is_empty(): return None` is the same "check-precondition-first" style you saw in `Cart.add_item` — fail fast and obviously, rather than letting an empty cart limp further into order construction and fail confusingly later.

```python
    def pay_for_order(self, user: User, order: Order) -> None:
        is_payment_success = order.process_payment()
        if is_payment_success:
            NotificationService.notify(order)
            user.get_cart().clear()
```

**Block-by-block:**

- This method is the clearest illustration of the whole Facade's job: **one call orchestrates three separate subsystems** — `Order.process_payment()` (which internally delegates to whatever `PaymentStrategy` is attached — Section 5), `NotificationService.notify()` (Section 9), and `Cart.clear()` (Section 3) — and the caller (`main.py`) only ever sees `tomato.pay_for_order(user, order)`. It doesn't know a Strategy pattern, a notification service, or a cart even exist.

**Theory — Facade pattern, and why it's arguably the most important pattern in this whole project:**

The **Facade pattern** provides a simplified, unified interface to a set of interfaces in a subsystem, hiding its complexity from the client. It doesn't add new functionality — every single thing `TomatoApp` does, you *could* do yourself by calling `RestaurantManager`, `Cart`, `OrderFactory`, `NotificationService` directly. The value is entirely about **reducing coupling**: `main.py` (and, if you built one, a REST controller, or a CLI menu, or a test suite) depends on exactly one class, with five or six clearly-named methods, instead of depending on eight classes scattered across five packages.

This matters enormously for **change management** in a real codebase. Say tomorrow you decide `OrderManager` should be backed by a real database instead of an in-memory list. If callers all over your codebase called `OrderManager.get_instance().add_order(...)` directly, you'd need to hunt down every call site. Because only `TomatoApp.checkout` ever touches `OrderManager`, you change exactly one method in exactly one file, and every caller of `TomatoApp` is completely unaffected.

This is also precisely the design that makes it easy to add a new "front end" later — a REST API, a CLI menu system, a chatbot interface — without touching any business logic: each new front end just calls the same handful of `TomatoApp` methods.

**How to reuse this elsewhere:** any time an LLD spec has multiple manager/service classes and also implies "a user interacts with the system" (an ATM, a library system, a vending machine, a parking lot), you almost always want one `Facade`/`System`/`Controller`-ish class at the top that's the single entry point — `ATM`, `LibrarySystem`, `VendingMachine`, `ParkingLot`. If your `main()` function is calling five different manager classes directly instead of one facade, that's usually a sign the facade is missing, not that it isn't needed.


---

## 11. `main.py` — the composition root

**Responsibility:** be the *only* place in the entire codebase where the top-level pieces get wired together and the program actually starts running.

```python
def main() -> None:
    tomato = TomatoApp()

    user = User(101, "Aditya", "Delhi")
    print(f"User: {user.get_name()} is active.")

    restaurant_list = tomato.search_restaurants("Delhi")
    if not restaurant_list:
        print("No restaurants found!")
        return
    ...
    order = tomato.checkout_now(user, "Delivery", UpiPaymentStrategy("1234567890"))
    tomato.pay_for_order(user, order)


if __name__ == "__main__":
    main()
```

**Block-by-block:**

- `tomato = TomatoApp()` — this single line is where the entire object graph for this program gets constructed (which, transitively, seeds the restaurants and initializes the two Singletons the first time `get_instance()` is called inside them). Nothing above this in the codebase constructs a `TomatoApp` — this genuinely is the one and only place it happens.
- `UpiPaymentStrategy("1234567890")` is constructed **right here, inline**, and handed to `checkout_now`. This is the concrete illustration of "Strategy objects get chosen and injected by the caller, not decided by the class that uses them" — `TomatoApp.checkout` has no idea whether it's UPI, credit card, or net banking; `main.py` decided that, at the last possible moment, and handed in the finished object.
- `if __name__ == "__main__": main()` is a Python idiom, not something Java has a direct equivalent of: it means "only run `main()` if this file was executed directly (`python3 main.py`), not if it was imported as a module from somewhere else." This makes the file safely importable — e.g., a test file could `from main import main` without accidentally triggering the whole simulation to run.

**Theory — the "Composition Root" pattern:**

A **composition root** is the single, specific place in an application where the object graph is built — where concrete classes actually get instantiated and wired to each other via constructor calls. Every other part of the codebase should depend on *abstractions* (interfaces, or at minimum, well-encapsulated classes reached through a facade) and never construct its own dependencies from scratch. In this project, `main.py` is that root: it's the only file that does `TomatoApp()`, `User(...)`, and `UpiPaymentStrategy(...)` at the top level of a script, as opposed to inside some other class's method (where `TomatoApp._initialize_restaurants` constructs `Restaurant`/`MenuItem` — but that's *within* the facade's own internal setup, not scattered across unrelated files).

Why this matters at scale: if construction logic is scattered everywhere (some class deep in a call stack decides to `import` and instantiate a concrete `NetBankingPaymentStrategy` on its own), you lose the ability to swap implementations centrally — e.g., for testing, you can't easily substitute a `FakePaymentStrategy` that always succeeds without hunting down every place a real strategy gets constructed. Keeping construction concentrated at the root is what makes dependency injection (mentioned in Section 7) practical in bigger systems.

**How to reuse this elsewhere:** in any LLD solution, structure your `main`/entry point the same way: construct the top-level facade/system object, construct any input data (users, initial catalog items), and then call a handful of methods on the facade — never let `main` reach three layers deep into internal classes directly.

---

## 12. SOLID principles — where each one shows up in this project

You've seen all five appear organically above; here they are consolidated, because interviewers often ask "name the SOLID principles and give me an example from your own code" as a direct question.

| Principle | What it means | Where it's applied here |
|---|---|---|
| **S** — Single Responsibility | A class should have exactly one reason to change | `NotificationService` only changes when *how you communicate* changes; `Order` only changes when *what an order is* changes. Kept deliberately separate (Section 9). |
| **O** — Open/Closed | Open for extension, closed for modification | `PaymentStrategy`: adding `NetBankingPaymentStrategy` required zero changes to `Order` or `TomatoApp` (Section 5). Same for `OrderFactory` (Section 8). |
| **L** — Liskov Substitution | A subclass must be usable anywhere its base class is expected, without breaking anything | Anywhere the code expects an `Order` (e.g. `OrderManager.add_order(order: Order)`), a `DeliveryOrder` or `PickupOrder` works correctly with no special-casing — because both fully honor `Order`'s contract (`get_type()`, `process_payment()`, all the getters) rather than, say, throwing an error from an inherited method they don't actually support. |
| **I** — Interface Segregation | Don't force a class to implement methods it doesn't need | `PaymentStrategy` has exactly **one** method (`pay`). If it also forced every strategy to implement `refund()`, `get_saved_cards()`, `verify_otp()`, etc., `UpiPaymentStrategy` would be stuck implementing (or stubbing out) methods that make no sense for it. Keeping the interface to the one method every implementer genuinely needs is ISP in action. |
| **D** — Dependency Inversion | Depend on abstractions, not concrete implementations | `TomatoApp.checkout(self, ..., order_factory: OrderFactory)` depends on the **abstract** `OrderFactory` type, never on `NowOrderFactory` or `ScheduledOrderFactory` by name. `Order.process_payment` depends on the **abstract** `PaymentStrategy`, never on `UpiPaymentStrategy` by name. (Where this project *doesn't* fully follow DIP: `TomatoApp` calls `RestaurantManager.get_instance()` and `OrderManager.get_instance()` directly — a concrete Singleton access point, not an injected abstraction. That's the honest trade-off flagged in Section 7.) |


---

## 13. Pattern-recognition cheat sheet — how to spot which pattern a *new* problem needs

This is the part meant to generalize beyond this specific project. When you get handed a new LLD problem — parking lot, splitwise, elevator system, chess, BookMyShow — run through this checklist. It's the same checklist that produced every design decision above.

**Step 1 — find the nouns.** List every "thing" the domain talks about. These become your model classes (Section 1–4, 6). Ask of each: does it have its own identity (needs an ID) or is it just a value (like `MenuItem`, meaningful only in context)? Does it own another object via composition, or just reference one via aggregation (Section 4)?

**Step 2 — find the words "different kinds of" or "different ways of."** *"Different kinds of accounts"* (savings vs. current), *"different kinds of vehicles,"* *"different ways to calculate a fare"* → these are candidates for either:
- **Inheritance + abstract base class** (Section 6) if the "different kinds" mostly share state/behavior and differ in a specific overridable piece — like `Order` → `DeliveryOrder`/`PickupOrder`.
- **Strategy pattern** (Section 5) if the "different ways" are a swappable *behavior* that a single object holds a reference to and can change at runtime — like `PaymentStrategy`.

  Quick test to tell them apart: if you'd naturally say "a `DeliveryOrder` **is a** kind of `Order`," that's inheritance. If you'd naturally say "an `Order` **has a** payment method it's currently using," that's Strategy (composition).

**Step 3 — find construction logic that branches on a type flag.** Any time you're about to write `if type == "X": return XThing() elif type == "Y": return YThing()` — that's Factory Method territory (Section 8). Pull it into its own factory class/hierarchy instead of leaving it inline in whatever method needed the object.

**Step 4 — find the words "there is only one" or "system-wide" / "global."** *"There is one elevator control system," "one parking lot manager," "one central ledger"* → Singleton (Section 7). Also immediately think about whether dependency injection would be a better answer to mention as the trade-off-aware alternative.

**Step 5 — find "the user interacts with the system by..."** Whatever verbs follow that phrase (book a ticket, park a car, place an order, split a bill) become the public methods of your top-level Facade class (Section 10) — the one class your `main()` actually talks to.

**Step 6 — sanity-check with SOLID after the first draft.** Once you have a rough class list, go through the table in Section 12 and ask of your own design: *if I add a new payment method / new vehicle type / new notification channel tomorrow, which files do I have to open?* If the answer is "just one new file," you've applied Open/Closed correctly. If the answer is "I have to edit this big existing class," that's your signal to introduce Strategy or Factory Method there.

---

## 14. A worked example — applying this exact framework to a *different* problem

To prove this generalizes, here's the same six-step process applied cold to a **parking lot** LLD, without writing the code — just to show the thinking transfers directly:

1. **Nouns:** `Vehicle` (has-a license plate — value-ish, identity via plate), `ParkingSpot` (has an ID, a size), `Ticket` (has an ID, entry time — needs an auto-incrementing ID, same `itertools.count` idiom as `Restaurant`/`Order`), `ParkingLot` (aggregates many `ParkingSpot`s, built elsewhere and handed in — aggregation, hollow diamond, like `RestaurantManager`/`Restaurant`).
2. **"Different kinds of":** "different kinds of vehicles" (motorcycle, car, bus, each needing a different spot size) → abstract `Vehicle` base class with concrete subclasses, exactly like `Order`/`DeliveryOrder`/`PickupOrder`. "Different ways to calculate the parking fee" (hourly vs. flat-rate vs. first-hour-free) → `FeeStrategy` interface with `calculate_fee(duration)`, exactly like `PaymentStrategy`.
3. **Type-flag construction:** issuing a `Ticket` differs slightly based on vehicle type or entry gate → a `TicketFactory`, exactly like `OrderFactory`.
4. **"Only one":** there's exactly one `ParkingLot` managing all spots app-wide → Singleton, exactly like `RestaurantManager`/`OrderManager` (and worth immediately noting to an interviewer: "though I'd consider injecting it instead, for testability").
5. **User-facing verbs:** "park a vehicle," "generate a bill," "free a spot" → these become the public methods on a `ParkingLotSystem` facade, exactly like `TomatoApp`.
6. **SOLID check:** adding a new vehicle type (say, "electric car with charging spot") should mean adding one `ElectricCar` subclass and maybe one new `FeeStrategy` — never editing `ParkingLotSystem` itself.

Every single pattern decision maps directly, because the *shape* of the reasoning ("what varies, what's shared, what's constructed dynamically, what's global, what's user-facing") is the same regardless of the domain. That transferable shape — not the food-delivery specifics — is the actual skill worth taking away from this project.

---

## 15. Quick reference — every pattern in this project, at a glance

| Pattern | Class(es) | One-line trigger phrase | The line of code that proves it |
|---|---|---|---|
| Singleton | `RestaurantManager`, `OrderManager` | "there is exactly one, app-wide" | `if cls._instance is None: cls._instance = cls()` |
| Strategy | `PaymentStrategy` + 3 implementations | "different ways to do X, swappable at runtime" | `self.payment_strategy.pay(self.total)` — `Order` never names a concrete strategy |
| Factory Method | `OrderFactory` + `NowOrderFactory`/`ScheduledOrderFactory` | "construction depends on a runtime type flag" | `def checkout(self, ..., order_factory: OrderFactory)` — caller injects *which* factory |
| Facade | `TomatoApp` | "the user interacts with the system by..." | `main.py` never imports `RestaurantManager`, `Cart`, or any factory directly |
| Abstract Base Class / Template-ish | `Order` → `DeliveryOrder`/`PickupOrder` | "different kinds of X that mostly share behavior" | `process_payment()` is concrete on `Order`; only `get_type()` is abstract |
| Composition | `User` → `Cart` | "X owns Y and Y can't outlive X" | `self._cart = Cart()` inside `User.__init__` |
| Aggregation | `RestaurantManager` → `Restaurant` | "X holds references to Y, but Y exists independently" | `def add_restaurant(self, restaurant: Restaurant)` — built elsewhere, handed in |

---

That's every file, every design decision, and the reasoning that should transfer to your next LLD problem. The single habit worth building from this: before writing a class, ask which row of that last table you're in — it tells you the shape of the solution before you write a line of code.

---

# Part II — Everything Section I skipped: the full concept map

Section 4 covered composition and aggregation because those two are directly visible in the code as "which class constructs which." But your diagram and this codebase actually use the **full standard set of UML relationships**, plus several OOP/design theory topics that were implicit in the explanations above but never named and defined on their own. This part fills every one of those gaps, explicitly, so nothing is left unlabeled.

---

## 16. The complete UML relationship spectrum (not just composition/aggregation)

Standard UML defines **six** relationship types between classes, ordered here from loosest coupling to tightest. Composition and aggregation (Section 4) are actually the two tightest, most specific kinds of a broader relationship called **association** — so this section is Section 4's missing context, not a repeat of it.

### 16.1 Dependency — the loosest relationship ("uses-a," temporarily)

**Definition:** class A depends on class B if a change to B's public interface *could* force a change in A, but A doesn't hold a lasting reference to B — it only touches B briefly, usually as a local variable inside a method, a method parameter, or a return type.

**In this codebase:** `TomatoApp._initialize_restaurants` creates `MenuItem` objects and immediately hands them to `restaurant.add_menu_item(...)` — `TomatoApp` never *stores* a reference to those `MenuItem` objects itself; it uses them transiently to set something up, then lets go. That's a dependency, not an association: `TomatoApp` needs `MenuItem` to exist and to have a working constructor, but doesn't have a lasting `self._menu_item = ...` field pointing at one.

**UML notation:** a dashed line with an open arrowhead, pointing from the dependent class to the class it depends on.

**Why it's worth naming separately from association:** it tells you how *hard* it would be to remove the relationship. Dependencies are cheap to change — swap out the type of a method parameter, and only the call sites need updating. Associations (next) are more expensive, because the reference is held long-term as a field.

### 16.2 Association — a lasting "knows-a" reference, no ownership implied

**Definition:** class A holds a reference to class B as an instance field, for the lifetime of A, but neither class owns the other's lifecycle — both could exist independently, and either could be deleted without necessarily destroying the other.

**In this codebase — this is the one that was missing from Section 4:** `Order.user` and `Order.restaurant`. An `Order` holds a long-lived reference to the `User` who placed it and the `Restaurant` it was placed with:

```python
# models/order.py
def set_user(self, user: "User") -> None:
    self.user = user

def set_restaurant(self, restaurant: "Restaurant") -> None:
    self.restaurant = restaurant
```

This is **association**, not composition and not aggregation, because:
- It's clearly not composition — the `User` was not created by the `Order` (`self.user = User()` never appears anywhere), and the `User` obviously outlives any single order they place (they can place ten more after this one).
- It's arguably not even aggregation in the strict "whole-part" sense either — a `User` isn't a *part* of an `Order` the way a `MenuItem` is part of a restaurant's menu or a `Restaurant` is part of `RestaurantManager`'s collection. An `Order` simply *references* a `User`, the way a `Reservation` references a `Guest`, or a `Transaction` references an `Account`. That "simple reference, no whole-part relationship" case is exactly what plain association is for.

**UML notation:** a solid line with no arrowhead (or a thin open arrowhead if the direction matters — i.e., `Order` knows about `User`, but does `User` need to know about every `Order` it placed? In this codebase, no — `User` has no `orders` field, so this is a **unidirectional** association: `Order → User`, one-way only).

**Rule of thumb to classify any reference you write:** ask two questions, in order:
1. *Does one object own the other's lifecycle* (created by it, dies with it)? → **Composition**.
2. *If not, is one object a "collection/whole" and the other a "part," even though the part could outlive the collection* (e.g., a restaurant removed from `RestaurantManager` doesn't stop existing)? → **Aggregation**.
3. *If neither of the above — it's just "I hold a reference to you because I need to look you up"* → **Association**.

### 16.3 Generalization / Inheritance — the "is-a" relationship

**Definition:** a specialized class (subclass) inherits the structure and behavior of a general class (superclass), and can be used anywhere the superclass is expected (this is also the Liskov Substitution Principle from Section 12).

**In this codebase:** `DeliveryOrder(Order)` and `PickupOrder(Order)` (Section 6). A `DeliveryOrder` **is an** `Order`. This is the *only* relationship in this list implemented in Python using the `class X(Y):` syntax itself — every other relationship (association, aggregation, composition, dependency) is implemented the same way in code: by one class holding a reference to another as a field, a parameter, or a local variable. Generalization is structurally distinct at the language level; the rest are only distinct *conceptually*.

**UML notation:** a solid line with a **hollow (unfilled) triangle arrowhead**, pointing from the subclass up to the superclass. On your uploaded diagram, this is exactly the arrow shape connecting `DeliveryOrder`/`PickupOrder` up to `Order`, and `CreditCard`/`NetBanking`/`UPI` up to `IPaymentStrategy`... except — see the next section — that second one is actually a *different* relationship wearing a similar-looking arrow.

### 16.4 Realization / Implementation — the "implements-a" relationship

**Definition:** a class provides a concrete implementation for an interface's contract. This looks almost identical to generalization in meaning ("is-a" in a loose sense) but applies specifically to interfaces rather than concrete/abstract classes with shared state.

**In this codebase:** `CreditCardPaymentStrategy`, `UpiPaymentStrategy`, and `NetBankingPaymentStrategy` each **realize** `PaymentStrategy`. Similarly, `NowOrderFactory` and `ScheduledOrderFactory` realize `OrderFactory`. Contrast this with `DeliveryOrder`/`PickupOrder` realizing... no, wait — `Order` isn't a pure interface (it has state and a concrete method, `process_payment`), so that relationship is generalization, not realization. But `PaymentStrategy` genuinely has *zero* shared state and *zero* shared implementation — pure contract — which is what makes `CreditCardPaymentStrategy → PaymentStrategy` realization rather than generalization.

**UML notation:** a **dashed** line with a hollow triangle arrowhead (as opposed to generalization's *solid* line with the same hollow triangle). Your diagram uses exactly this: look closely at the arrows from `CreditCard`/`NetBanking`/`UPI` up to `IPaymentStrategy` — they're drawn dashed, while the arrow from `DeliveryOrder`/`PickupOrder` up to `Order` is drawn solid. That's not a stylistic accident; it's the diagram correctly distinguishing realization from generalization, because `IPaymentStrategy` is explicitly labeled `<<Interface>>` on your diagram, while `Order` is not.

**In Python specifically:** both generalization and realization are written with the exact same syntax (`class X(Y):`), because Python doesn't have a separate `implements` keyword the way Java does. The *only* way to tell them apart in Python code is to check whether the parent class is a "pure" `ABC` with no shared state (realization) or has real fields and concrete methods (generalization) — which is exactly the distinction made in Section 6's theory box about `Order` vs `PaymentStrategy`, now given its formal UML name.

### 16.5 & 16.6 Aggregation and Composition — already covered, now placed in context

These are Section 4's content, re-anchored into the full spectrum: both are **specialized kinds of association** that add a "whole-part" (has-a, made-of) meaning on top of plain association's "just holds a reference" meaning. Composition adds a further constraint on top of aggregation: the part's lifecycle is bound to the whole's.

**UML notation, to complete the set:** aggregation is a solid line with a **hollow (unfilled) diamond** at the "whole" end; composition is a solid line with a **filled (solid black) diamond** at the "whole" end. On your diagram, look at the diamond between `RestaurantManager` and `Restaurant` — it's drawn as a hollow/hatched diamond (aggregation: restaurants outlive the manager conceptually), versus a filled diamond you'd expect between `User` and `Cart` for composition.

### Summary table — all six, side by side, with this project's example for each

| Relationship | Meaning | Notation | Example in this project |
|---|---|---|---|
| Dependency | "uses-a," temporary, no stored reference | dashed line, open arrowhead | `TomatoApp` constructing a `MenuItem` inline and handing it off |
| Association | "knows-a," stored reference, no ownership | solid line, no/thin arrowhead | `Order.user`, `Order.restaurant` |
| Aggregation | "has-a" (whole-part), part outlives the whole | solid line, hollow diamond | `RestaurantManager` → `Restaurant` |
| Composition | "has-a" (whole-part), part dies with the whole | solid line, filled diamond | `User` → `Cart` |
| Generalization | "is-a," shares real state/behavior via inheritance | solid line, hollow triangle | `Order` → `DeliveryOrder`/`PickupOrder` |
| Realization | "implements-a," fulfills a pure-contract interface | dashed line, hollow triangle | `PaymentStrategy` → `UpiPaymentStrategy`, `OrderFactory` → `NowOrderFactory` |

**Multiplicity (the `(1...*)` labels on your diagram):** those numbers next to a relationship line describe *how many* of one object can be connected to *how many* of the other — this is called **multiplicity** or **cardinality**. `Restaurant (1...*) MenuItem` on your diagram means: one restaurant can have many (one-or-more) menu items, and (implicitly, reading the other end) each `MenuItem` belongs to exactly one restaurant. In code, multiplicity is what tells you whether a field should be a single reference (`self.restaurant: Restaurant`) or a collection (`self._menu: List[MenuItem]`) — every `List[...]` type hint you've seen throughout this codebase is a "many" multiplicity made concrete.

**The stereotypes on your diagram (`<<Singleton>>`, `<<Interface>>`, `<<Model>>`):** these double-angle-bracket labels are UML's way of tagging a class with a *role* that isn't part of the core UML vocabulary but is meaningful to your specific design. `<<Singleton>>` on `RestaurantManager`/`OrderManager` documents the pattern from Section 7 directly on the diagram. `<<Interface>>` on `IPaymentStrategy`/`IOrderFactory` documents that these are pure-contract ABCs (Section 6 and 16.4). `<<Model>>` on `Restaurant`/`MenuItem`/`User` is a lighter-weight stereotype meaning "this is a plain data-holding domain object," distinguishing them from manager/service/strategy classes on the same diagram. Stereotypes are optional but valuable exactly because UML's six formal relationship types don't capture *pattern intent* on their own — the diamond shape tells you "aggregation," but only the `<<Singleton>>` label tells you *why* `RestaurantManager` is drawn that way.


---

## 17. The four pillars of OOP — named explicitly, with every example already in this codebase pulled together

Each of these was demonstrated somewhere above but never collected under its formal name. Interviewers frequently ask "what are the four pillars of OOP, and can you point to an example in code you've written" — here's that answer, pre-built from this project.

### 17.1 Encapsulation

**Definition:** bundling data together with the methods that operate on it, and restricting direct access to that data from outside the class, so the class alone controls how its own state can change.

**Where it lives here:** every single model class (Section 1). `MenuItem._price` is never touched directly from outside — only through `get_price()`/`set_price()`. `Cart._items` is only ever modified through `add_item()`, which enforces the "must have a restaurant first" rule. Encapsulation is what makes it *possible* to add that rule in one place and trust it's enforced everywhere.

### 17.2 Abstraction

**Definition:** exposing only the essential, relevant details of an object's behavior while hiding the implementation complexity behind it. Where encapsulation is about *protecting* data, abstraction is about *simplifying* what a consumer needs to think about.

**Where it lives here, at two different scales:**
- **Small scale:** `Order.process_payment()` — the caller (`TomatoApp.pay_for_order`) just calls one method and gets back `True`/`False`. It doesn't need to think about *which* payment strategy is attached, how `pay()` is implemented, or what output format each strategy prints — all of that complexity is abstracted away behind one boolean-returning method.
- **Large scale:** `TomatoApp` itself (Section 10) is abstraction applied to an entire subsystem — `main.py` thinks about "search, select, add to cart, checkout, pay" and nothing else; the existence of `RestaurantManager`, `OrderManager`, three factory classes, and three strategy classes is completely abstracted away.

`ABC` and `@abstractmethod` (used throughout: `Order`, `PaymentStrategy`, `OrderFactory`) are Python's *formal, enforced* tool for abstraction — they let you define "this is the essential contract, implementation details go in the subclass" and have Python refuse to run if a subclass skips a required piece.

### 17.3 Inheritance

**Definition:** a mechanism where a new class derives fields and methods from an existing class, allowing shared behavior to be written once and reused (and, for LSP, substituted safely).

**Where it lives here:** `DeliveryOrder(Order)`, `PickupOrder(Order)` (Section 6) — both inherit `process_payment`, all the getters/setters, and the `_id_counter` scheme from `Order`, and only add what's genuinely new (`_user_address` / `_restaurant_address`). Also every strategy (`class UpiPaymentStrategy(PaymentStrategy)`) and every factory (`class NowOrderFactory(OrderFactory)`) technically use inheritance syntax even where the *relationship* is realization rather than generalization (Section 16.4) — a good reminder that "inheritance" is the Python/Java *language mechanism*, while "generalization" vs. "realization" is the *conceptual* label for what that mechanism is being used to express in a given case.

**The trade-off worth knowing:** inheritance creates **tight coupling** between a subclass and its superclass's internal implementation — if `Order.__init__` changes its parameter list, both `DeliveryOrder` and `PickupOrder` must change too, since they call `super().__init__()`. This is why the industry-standard advice is "favor composition over inheritance" whenever the relationship is closer to "has-a" than genuinely "is-a" — you saw this exact judgment call already: `PaymentStrategy` is attached to `Order` via composition (`self.payment_strategy`), *not* by making `CreditCardOrder` and `UpiOrder` subclasses of `Order` — because payment method can change independently and isn't a fundamental "kind of order," while Delivery-vs-Pickup genuinely is.

### 17.4 Polymorphism

**Definition:** the ability to call the same method name on different objects and have each one respond according to its own specific implementation — "many forms" for one interface.

**Where it lives here, in two flavors:**
- **Runtime/subtype polymorphism (the common case):** `payment_strategy.pay(amount)` inside `Order.process_payment()` — depending on *which* concrete `PaymentStrategy` object is currently attached, this one line of code produces completely different behavior (UPI message vs. credit card message vs. net banking message), decided entirely at runtime based on which object was assigned.
- **Duck typing (Python-specific, worth naming since it doesn't exist the same way in Java):** Python doesn't strictly require an object to inherit from `PaymentStrategy` to be usable as one — if you handed `Order.set_payment_strategy` *any* object with a `.pay(amount)` method, it would work identically, `ABC` inheritance or not, because Python resolves `payment_strategy.pay(...)` by checking "does this object have a `pay` attribute that's callable" at the moment it's called, not by checking its declared type ahead of time. This is called **duck typing** — "if it walks like a duck and quacks like a duck, treat it like a duck." The `ABC`/`@abstractmethod` machinery in this codebase is used specifically to make the contract *explicit and enforced* rather than relying purely on duck typing, which is a deliberate, good practice for a codebase you want other people (or future you) to understand quickly — but it's worth knowing Python would still technically run without it.

### Where all four appear together, in one line, if you want the single "give me an example" answer

```python
self.payment_strategy.pay(self.total)
```

- **Encapsulation:** `self.total` and `self.payment_strategy` are accessed as instance attributes, only ever set through controlled setter methods elsewhere in the class.
- **Abstraction:** `Order` doesn't know or care what `pay()` actually *does* — only that it exists and takes an amount.
- **Inheritance/Realization:** `payment_strategy` is guaranteed to have `.pay()` because whatever concrete class it is, it inherited from (realized) `PaymentStrategy`.
- **Polymorphism:** the actual behavior that runs when this line executes depends entirely on which concrete object `payment_strategy` currently refers to.


---

## 18. Design pattern categories — where this project's four patterns sit in the bigger Gang-of-Four picture

The 1994 "Gang of Four" book (*Design Patterns: Elements of Reusable Object-Oriented Software*) organizes all 23 classic design patterns into three categories, based on *what kind of problem* they solve. Knowing the category — not just the individual pattern name — is what lets you guess the *right family* of pattern to reach for on a brand-new problem, even one you've never seen a named pattern for.

### Creational patterns — "how do I construct objects flexibly, instead of hardcoding `new`/`ClassName()` everywhere?"

Used in this project: **Singleton** (Section 7) and **Factory Method** (Section 8).

Other patterns in this family, worth recognizing by name even though they're not in this project: **Abstract Factory** (families of related factories — see the distinction drawn in Section 8's theory box), **Builder** (constructing a complex object step-by-step, useful when a constructor would otherwise need ten optional parameters — imagine building an `Order` with optional discount codes, optional gift wrapping, optional special instructions, one `.with_x()` call at a time), **Prototype** (creating new objects by cloning an existing one instead of building from scratch, useful when construction is expensive).

### Structural patterns — "how do I compose classes and objects into larger structures while keeping them loosely coupled?"

Used in this project: **Facade** (Section 10).

Other patterns in this family: **Adapter** (translate one class's interface into another interface a client expects — e.g., if you integrated a real third-party payment gateway with a totally different method signature than `PaymentStrategy.pay(amount)`, you'd write an Adapter class that wraps the gateway's SDK and exposes it as a `PaymentStrategy`), **Decorator** (attach additional responsibilities to an object dynamically — e.g., wrapping an `Order` with a `GiftWrappedOrder` decorator that adds cost without subclassing `Order` itself), **Composite** (treat individual objects and groups of objects uniformly — common in file-system-like or menu-with-subcategories LLD problems), **Proxy** (a stand-in object that controls access to another object — e.g., a `CachedRestaurantManager` proxy that checks a cache before hitting the real one).

### Behavioral patterns — "how do objects communicate and distribute responsibility for a task among themselves?"

Used in this project: **Strategy** (Section 5).

Other patterns in this family: **Observer** (objects subscribe to be notified when another object's state changes — this is the natural *next step* for `NotificationService`: instead of `TomatoApp.pay_for_order` explicitly calling `NotificationService.notify(order)`, an `Order` could maintain a list of "observers" — an email notifier, an SMS notifier, an analytics logger — and notify all of them automatically the moment its state changes to "paid," without `TomatoApp` needing to know how many listeners exist), **State** (an object changes its behavior when its internal state changes — directly relevant to the "add an order status: PENDING → CONFIRMED → CANCELLED" idea flagged in the very first response about this project: each state could be its own class with its own allowed transitions, instead of one big `if status == "PENDING":` chain), **Command** (encapsulate a request as an object, useful for undo/redo or queuing — e.g., wrapping "place this order" as a `PlaceOrderCommand` object that can be logged, retried, or queued), **Template Method** (already referenced in Section 6's theory box — a base class defines the skeleton of an algorithm and lets subclasses override specific steps; the honest refactor note in Section 8 about de-duplicating the two `OrderFactory` implementations is literally "apply Template Method here").

### Why the categorization matters more than memorizing all 23 names

If a new LLD problem needs "a flexible way to build objects" — you now know to *start* by asking "is this Factory Method (one product, decided by a flag) or Builder (one product, assembled step-by-step) or Abstract Factory (a coordinated family of products)" rather than blanking on pattern names. If it needs "objects reacting to another object's changes" — you go straight to Observer, without needing to have seen that exact problem before. The category is the searchable index; the specific pattern name is just where you land inside it.


---

## 19. Coupling and cohesion — the two metrics every design decision above was actually optimizing for

Every pattern discussion above (Strategy for Open/Closed, Facade for a single entry point, Singleton's DI trade-off) was really a discussion about these two properties. They're worth naming directly because they're the actual *criteria* you use to judge whether a design is good, independent of which named pattern you used to get there.

**Coupling** — how much one class *depends on the internal details* of another. **Low coupling** (good) means you can change one class without rippling changes into others. **High coupling** (bad) means classes are tangled together such that touching one breaks or requires changing several others.

- *Low coupling example in this project:* `Order.process_payment()` is coupled only to the *abstract* `PaymentStrategy` interface (one method: `pay`), not to any concrete strategy. You can add, remove, or completely rewrite `UpiPaymentStrategy` and `Order` never needs to change.
- *Higher coupling, honestly present in this project:* `TomatoApp` is directly coupled to the *concrete* `RestaurantManager` and `OrderManager` classes (calling `.get_instance()` on each by name) rather than to abstractions of them — this is exactly the Dependency Inversion gap flagged in Section 12's SOLID table.

**Cohesion** — how closely the responsibilities *within* a single class relate to one another. **High cohesion** (good) means every method and field in a class exists in service of one clear purpose. **Low cohesion** (bad) means a class is a grab-bag of loosely related responsibilities that happen to be bundled together.

- *High cohesion example:* `Cart` — every method (`add_item`, `get_total_cost`, `is_empty`, `clear`, `set_restaurant`) exists purely to manage "what's currently being ordered." Nothing in `Cart` is about payment, notification, or restaurant search.
- *What low cohesion would look like, for contrast:* if `Cart` also had a `send_confirmation_email()` method, that would be low cohesion — email-sending has nothing to do with "managing a shopping cart's contents," and it would mean `Cart` now has two unrelated reasons to change (Single Responsibility Principle, Section 12, violated as a direct consequence).

**The relationship between the two:** good OOP design pushes toward **low coupling, high cohesion** — classes that are self-contained and focused internally, but talk to each other through narrow, abstract interfaces externally. Nearly every pattern in this document (Strategy, Factory Method, Facade) is a specific, named technique for achieving exactly that combination in a specific recurring situation. When you're not sure whether a design is "good," these two words are the actual test: *is this class doing one focused thing (cohesion), and does changing another class force me to change this one too (coupling)?*

---

## 20. The Law of Demeter ("don't talk to strangers") — and an honest look at where this project bends it

**Definition:** a method of object O should only call methods on: (1) O itself, (2) O's own fields, (3) objects passed as parameters to that method, or (4) objects it creates locally inside that method. It should **not** reach through one object to grab a second object and then call a method on *that* — chains like `a.get_b().get_c().do_thing()` are the textbook violation, because `a`'s caller now implicitly depends on the internal structure of `b` too, not just `a`'s own public interface.

**Where this project actually bends the rule — worth knowing exactly where and why, rather than pretending it doesn't happen:**

```python
# tomato_app.py
def select_restaurant(self, user: User, restaurant: Restaurant) -> None:
    user.get_cart().set_restaurant(restaurant)
```

```python
# tomato_app.py
def add_to_cart(self, user: User, item_code: str) -> None:
    restaurant = user.get_cart().get_restaurant()
```

Both of these are `user.get_cart().<do something>()` — reaching through `User` to get its `Cart`, then immediately calling a method on that `Cart`. Strictly by the letter of the Law of Demeter, this is a violation: `TomatoApp` now needs to know that `User` has a `Cart`, and that `Cart` has a `set_restaurant`/`get_restaurant` method — two "hops" of knowledge instead of one.

**Why this is a defensible, common exception rather than a real problem:** the Law of Demeter is explicitly a *guideline*, not an absolute rule, and virtually every real Python/Java codebase breaks it for simple, well-encapsulated getter chains like this one. The stricter, fully-compliant alternative would be to add pass-through methods directly on `User` — `user.set_cart_restaurant(restaurant)`, `user.get_cart_restaurant()` — that internally forward to `self._cart.set_restaurant(...)`. This *does* reduce coupling further, but at the cost of `User` accumulating a growing pile of forwarding methods for every single thing you might ever want to do to its cart — which can hurt cohesion (Section 19) more than the coupling it saves. This is a genuine, debatable trade-off, and "I know this line technically bends the Law of Demeter, and here's why I judged it an acceptable trade-off rather than an oversight" is a materially stronger answer in an interview than either not noticing it or reflexively "fixing" every chained call without weighing the cost.

**Where it's worth actually fixing, as a rule of thumb:** the deeper the chain, and the more that chain appears repeated across many call sites, the more it's worth collapsing into a proper method. A two-hop chain (`user.get_cart().set_restaurant(...)`) used in two places is a judgment call either way. A three-or-more-hop chain (`order.get_user().get_cart().get_restaurant().get_location()`) repeated across a dozen call sites is a strong signal that a proper forwarding method — or, in this case, whichever intermediate class actually owns that concern — is genuinely missing.

---

## 21. DRY and YAGNI — the two principles behind the honest "this could be refactored" notes above

**DRY — Don't Repeat Yourself:** every piece of knowledge should have a single, unambiguous representation in a system. This is the principle behind the refactor note in Section 8: `NowOrderFactory.create_order` and `ScheduledOrderFactory.create_order` duplicate the entire Delivery-vs-Pickup branching logic and every setter call except one line. That's the same piece of knowledge ("how to assemble an `Order` from its parts") expressed twice — if a new required field got added to `Order` tomorrow, you'd have to remember to update *both* factory files identically, and it's exactly the kind of thing that's easy to update in one file and forget in the other, producing a subtle, hard-to-spot bug.

**YAGNI — You Aren't Gonna Need It:** don't build flexibility or abstraction for a requirement you don't actually have yet, on the speculation that you might need it later. This is the principle that explains why this project's honest imperfections were *left in* rather than "gold-plated" away:

- The `OrderFactory` duplication *could* be refactored into a shared Template Method base right now — but doing so before you actually have a third or fourth factory type (recurring orders? group orders?) is speculative complexity paid for upfront, for a benefit you don't yet know you need. DRY says "this duplication is a smell, keep an eye on it." YAGNI says "don't necessarily fix it yet, especially if the fix would make the current two-factory case harder to read for the sake of a hypothetical third case."
- Similarly, `RestaurantManager`/`OrderManager` staying as Singletons instead of being refactored into dependency-injected objects (Section 7) is a reasonable YAGNI call for a project this size — the DI refactor pays off once you have, say, a test suite that needs to inject fake managers, or multiple `TomatoApp` instances running independently. Until one of those needs actually exists, the Singleton is simpler and does the job.

**The productive tension between DRY and YAGNI, worth being able to articulate:** DRY pulls toward "abstract this now, before it duplicates further." YAGNI pulls toward "don't abstract until the second or third real use case actually shows up, because premature abstraction is its own kind of technical debt — often *worse* than duplication, because the wrong abstraction is harder to undo than a few repeated lines." A useful rough heuristic some engineers use: duplicate something once without worrying about it; the *second* time you're about to duplicate the same logic a third time, that's usually the signal DRY has "earned" the refactor and YAGNI no longer applies.


---

## 22. Python-specific mechanics used throughout — named and compared directly

These appeared repeatedly across every file above without being gathered into one place for direct comparison. If you're translating between Java and Python regularly (which you are), these are the recurring "same concept, different syntax/behavior" points worth having crisp.

### 22.1 `@staticmethod` vs `@classmethod` vs a plain instance method

All three appear in this project — side by side, they clarify each other:

```python
# instance method — needs a specific object's own state (self)
def get_price(self) -> int:            # MenuItem
    return self._price

# classmethod — needs the class itself, not any specific instance (cls)
@classmethod
def get_instance(cls) -> "RestaurantManager":   # RestaurantManager, Section 7
    if cls._instance is None:
        cls._instance = cls()
    return cls._instance

# staticmethod — needs neither; it's just a function namespaced inside the class
@staticmethod
def notify(order: Order) -> None:       # NotificationService, Section 9
    ...
```

- **Instance method** (no decorator, first parameter `self`): operates on one specific object's data. Almost every method on `MenuItem`, `Restaurant`, `Cart`, `User`, `Order` is this kind — they all read or write `self._something`.
- **`@classmethod`** (first parameter `cls`, the class itself): used when a method needs to know *which class it belongs to* but doesn't need any particular instance — the canonical use case is exactly what `RestaurantManager.get_instance` and `OrderManager.get_instance` do: create-or-return "the one instance of this class," which by definition can't take `self`, because at the moment it's called there might not be an instance yet.
- **`@staticmethod`** (no special first parameter at all): used when a method logically *belongs* inside a class (for organization/namespacing) but touches no instance state and no class state either — `NotificationService.notify` and `TimeUtils.get_current_time` are both this: pure functions that happen to live inside a class because grouping related utility functions under one name is convenient, not because they need `self` or `cls` for anything.

**How to choose, fast:** does the method need `self._some_field`? → instance method. Does it need to create/look up something scoped to the whole class, like a singleton or a counter? → classmethod. Does it need neither? → staticmethod (and honestly, ask whether it should just be a plain module-level function instead of being inside a class at all — Python doesn't require everything to live in a class the way Java does).

### 22.2 `ABC` + `@abstractmethod` — Python's opt-in enforcement for interfaces/abstract classes

Covered in depth in Section 5 and 6 — collected here just to name the mechanism itself clearly: Python, unlike Java, does not have a built-in `interface` or `abstract` keyword. `ABC` (from the standard library's `abc` module) and `@abstractmethod` are how Python *simulates* that enforcement — a class inheriting from `ABC` with at least one `@abstractmethod` cannot be instantiated directly, and any subclass that doesn't override every abstract method also can't be instantiated. This is opt-in: nothing stops you from writing plain classes with no `ABC` at all and relying purely on duck typing (Section 17.4) — using `ABC` is a deliberate choice to make a contract explicit and machine-enforced rather than just a naming convention.

**The newer alternative worth knowing about — `typing.Protocol` (structural typing):**

```python
from typing import Protocol

class PaymentStrategy(Protocol):
    def pay(self, amount: float) -> None: ...
```

With `Protocol` (Python 3.8+), you get *static-analysis-time* checking (a type checker like `mypy` will flag a class that doesn't match the shape) **without** requiring explicit inheritance — any class with a matching `pay(self, amount: float) -> None` method satisfies the protocol automatically, even if it never wrote `class X(PaymentStrategy)`. This is Python leaning fully into duck typing, formalized. `ABC` says "you must explicitly declare you implement this contract, and Python will check at runtime." `Protocol` says "if it has the right shape, it counts, checked only by your type checker, not at runtime." This project uses `ABC` throughout because explicit, runtime-enforced contracts are usually the better teaching and interview choice — but knowing `Protocol` exists, and why you might reach for it in a large real codebase with many independent teams (nobody has to import your base class just to be compatible with it), is worth having in your pocket.

### 22.3 Type hints, `Optional`, and forward references — what they buy you (and what they don't)

`Optional[Restaurant]`, `List[MenuItem]`, `-> bool` throughout this codebase are **type hints** — they document expected types and let external tools (`mypy`, your IDE) catch mismatches *before* running the code. Critically: **Python does not enforce these at runtime.** `def pay(self, amount: float)` will happily accept a string if you call `pay("oops")` — nothing crashes until whatever line inside `pay` tries to actually use `amount` as a number. This is the single biggest mental adjustment coming from Java, where a type mismatch is a compile error, full stop. In Python, type hints are a documentation-and-tooling layer, not a language guarantee — which is exactly why the `ABC` runtime enforcement discussed above matters more in Python than the equivalent would in Java: Java's compiler already catches "you didn't implement this interface method" for you; Python needs `ABC` to catch the analogous mistake, because plain type hints alone won't.

`Optional[X]` is shorthand for `Union[X, None]` — "this could be an `X`, or it could be `None`." Every place you saw it (`Cart._restaurant: Optional[Restaurant] = None`) is documenting exactly the same thing Section 3 called out conceptually: this field has a valid "not set yet" state, and any code touching it needs to handle both possibilities.

The `TYPE_CHECKING` + string-quoted hints (`"User"`, `"PaymentStrategy"`) in `models/order.py`, explained in Section 6, exist purely to avoid circular imports at runtime while still giving type checkers full information — worth remembering as a named, reusable trick rather than a one-off oddity, because it comes up in any medium-sized Python codebase where two modules would otherwise need to import each other.


---

## 23. Updated quick-reference table — every concept in this document, in one place

| # | Concept | Category | Where it lives in this project |
|---|---|---|---|
| 1 | Encapsulation | OOP pillar | Every model's `_field` + getter/setter |
| 2 | Abstraction | OOP pillar | `Order.process_payment()`, `TomatoApp` as a whole |
| 3 | Inheritance | OOP pillar / UML relationship | `DeliveryOrder(Order)`, `PickupOrder(Order)` |
| 4 | Polymorphism (subtype) | OOP pillar | `payment_strategy.pay(...)` behaving differently per concrete strategy |
| 5 | Polymorphism (duck typing) | OOP pillar / Python-specific | Any object with `.pay()` works, `ABC` or not |
| 6 | Dependency | UML relationship | `TomatoApp` constructing a `MenuItem` transiently |
| 7 | Association | UML relationship | `Order.user`, `Order.restaurant` |
| 8 | Aggregation | UML relationship | `RestaurantManager` → `Restaurant` |
| 9 | Composition | UML relationship | `User` → `Cart` |
| 10 | Generalization | UML relationship | `Order` → `DeliveryOrder`/`PickupOrder` |
| 11 | Realization | UML relationship | `PaymentStrategy` → `UpiPaymentStrategy`; `OrderFactory` → `NowOrderFactory` |
| 12 | Multiplicity / cardinality | UML notation | `Restaurant (1...*) MenuItem` |
| 13 | Stereotypes (`<<Singleton>>` etc.) | UML notation | Labels on your uploaded diagram |
| 14 | Singleton | Creational pattern | `RestaurantManager`, `OrderManager` |
| 15 | Factory Method | Creational pattern | `OrderFactory`, `NowOrderFactory`, `ScheduledOrderFactory` |
| 16 | Facade | Structural pattern | `TomatoApp` |
| 17 | Strategy | Behavioral pattern | `PaymentStrategy` + 3 implementations |
| 18 | Template Method (implied refactor) | Behavioral pattern | Suggested fix for factory duplication |
| 19 | Observer (implied next step) | Behavioral pattern | Suggested evolution of `NotificationService` |
| 20 | State (implied next step) | Behavioral pattern | Suggested evolution of order status |
| 21 | SOLID — Single Responsibility | Principle | `NotificationService` isolated from `Order` |
| 22 | SOLID — Open/Closed | Principle | Adding `NetBankingPaymentStrategy` touches nothing else |
| 23 | SOLID — Liskov Substitution | Principle | `DeliveryOrder`/`PickupOrder` fully honor `Order`'s contract |
| 24 | SOLID — Interface Segregation | Principle | `PaymentStrategy` has exactly one method |
| 25 | SOLID — Dependency Inversion | Principle | `checkout(..., order_factory: OrderFactory)` depends on the abstraction |
| 26 | Coupling | Design quality metric | Low: `Order`↔`PaymentStrategy`. Higher: `TomatoApp`↔concrete Singletons |
| 27 | Cohesion | Design quality metric | High: every `Cart` method is about cart management only |
| 28 | Law of Demeter | Design guideline | `user.get_cart().set_restaurant(...)` — a deliberate, judged exception |
| 29 | DRY | Principle | Flags the `OrderFactory` duplication as a smell |
| 30 | YAGNI | Principle | Explains why that duplication is defensibly left alone for now |
| 31 | Composition root | Architecture concept | `main.py` |
| 32 | Dependency Injection (the road not taken) | Architecture concept | Named as the alternative to Singleton's global access |
| 33 | `@staticmethod` / `@classmethod` / instance method | Python mechanics | `NotificationService.notify` / `get_instance` / any `get_x` method |
| 34 | `ABC` + `@abstractmethod` | Python mechanics | `Order`, `PaymentStrategy`, `OrderFactory` |
| 35 | `typing.Protocol` (the road not taken) | Python mechanics | Named as the structural-typing alternative to `ABC` |
| 36 | Type hints, `Optional`, forward references | Python mechanics | Every method signature in the codebase |
| 37 | `itertools.count` ID idiom | Python mechanics | `Restaurant._id_counter`, `Order._id_counter` |
| 38 | Mutable class-attribute pitfall | Python mechanics | Why `_menu`/`_items` must be created in `__init__`, not as class attributes |

This table is the fastest way to review before an interview: cover the right column, and see if you can explain each concept from the left, cold, using this project as your example.

