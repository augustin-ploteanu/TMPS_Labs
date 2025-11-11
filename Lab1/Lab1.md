# **Lab 1: Creational Design Patterns**

## Theory

### **1. Singleton**

The **Singleton** pattern ensures that a class has only one instance throughout the application and provides a single, global access point to it. It’s commonly used for shared resources like configuration managers, loggers, or database connections. The pattern controls object creation internally, ensuring all code refers to the same instance, which simplifies global state management but can make testing and dependency management more difficult if overused.

### **2. Builder**

The **Builder** pattern separates the construction of a complex object from its representation, allowing the same construction process to produce different variations of the object. It’s useful when creating objects that require multiple steps or configurations, making code cleaner and more flexible. By encapsulating object assembly logic, the builder avoids long constructors and improves readability and reusability.

### **3. Prototype**

The **Prototype** pattern creates new objects by cloning existing ones instead of constructing them from scratch. It’s ideal when object creation is resource-intensive or involves complex initialization. By copying a pre-existing prototype, this pattern enables efficient object creation and dynamic configuration, though it requires careful handling of deep versus shallow copies to prevent unintended side effects.

### **4. Object Pooling**

The **Object Pooling** pattern maintains a set of initialized, reusable objects instead of creating and destroying them repeatedly. When a client needs an object, it borrows one from the pool, and when done, it returns it for reuse. This approach significantly improves performance in systems where object creation is expensive, such as in database or network connections, but requires careful management to avoid concurrency issues or resource leaks.

### **5. Factory Method**

The **Factory Method** pattern defines an interface for creating objects but lets subclasses decide which specific class to instantiate. It encapsulates object creation logic, allowing new product types to be added without modifying existing code. This promotes flexibility, extensibility, and adherence to the Open/Closed Principle, making it ideal for frameworks or libraries that must create objects without knowing their exact types in advance.

### **6. Abstract Factory**

The **Abstract Factory** pattern provides an interface for creating families of related or dependent objects without specifying their concrete classes. It’s used when a system must be independent of how its objects are created, composed, or represented. By grouping related factories together, it ensures consistency among created products and simplifies switching between different configurations or environments, such as different UI themes or database backends.

---

Sure — here is the **updated section**, rewritten so that the **Prototype pattern is external** (using a registry instead of `clone()` inside `Pizza`).
The Factory and Builder sections stay the same — only the Prototype part changes.

---

## Implementation

### **1. Factory Method — Creating pizza objects**

`domain/factory/pizza_factory.py`

```python
from ..models.pizza import Pizza, margherita, pepperoni, veggie

class SimplePizzaFactory:
    _registry = {
        "margherita": margherita,
        "pepperoni": pepperoni,
        "veggie": veggie
    }

    def create(self, kind: str, size: str = "M") -> Pizza:
        key = kind.strip().lower()
        ctor = self._registry.get(key)
        if not ctor:
            raise ValueError(f"Unknown pizza type: {kind}")
        return ctor(size=size)
```

The client requests a pizza by type, and the factory returns the corresponding pizza instance.
This allows new pizza types to be added by updating the registry instead of rewriting logic in multiple places.

---

### **2. Prototype — Reusing Pizza Templates**

`domain/models/prototype.py`

```python
from __future__ import annotations
from copy import deepcopy
from typing import Dict
from .pizza import Pizza

class PrototypeRegistry:
    """Stores pizza templates and creates copies when requested."""
    def __init__(self):
        self._registry: Dict[str, Pizza] = {}

    def register(self, key: str, pizza: Pizza) -> None:
        self._registry[key.lower()] = pizza

    def clone(self, key: str) -> Pizza:
        try:
            return deepcopy(self._registry[key.lower()])
        except KeyError:
            raise ValueError(f"Unknown prototype: {key}")
```

A pizza can be registered once and cloned whenever a similar version is needed.
The cloned pizza can then be customized (for example, adding toppings) without modifying the original.
Deep copying ensures that lists such as `toppings` are duplicated rather than shared.

---

### **3. Builder — Constructing Order Objects**

`domain/models/order_builder.py`

```python
from dataclasses import dataclass, field
from typing import List, Optional
from .pizza import Pizza

@dataclass
class Order:
    customer: str
    address: Optional[str]
    pizzas: List[Pizza] = field(default_factory=list)
    note: Optional[str] = None
    coupon_pct: float = 0.0
    contactless: bool = False

    def total(self) -> float:
        subtotal = sum(p.price() for p in self.pizzas)
        discount = subtotal * (self.coupon_pct / 100)
        return round(subtotal - discount, 2)

class OrderBuilder:
    def __init__(self, customer: str):
        self._customer = customer
        self._address = None
        self._pizzas: List[Pizza] = []
        self._note = None
        self._coupon_pct = 0.0
        self._contactless = False

    def deliver_to(self, address: str) -> "OrderBuilder":
        self._address = address
        return self

    def add_pizza(self, pizza: Pizza) -> "OrderBuilder":
        self._pizzas.append(pizza)
        return self

    def with_coupon(self, pct: float) -> "OrderBuilder":
        self._coupon_pct = pct
        return self

    def with_note(self, note: str) -> "OrderBuilder":
        self._note = note
        return self

    def contactless_delivery(self, enabled: bool = True) -> "OrderBuilder":
        self._contactless = enabled
        return self

    def build(self) -> Order:
        return Order(
            customer=self._customer,
            address=self._address,
            pizzas=list(self._pizzas),
            note=self._note,
            coupon_pct=self._coupon_pct,
            contactless=self._contactless
        )
```

The Builder allows the client to construct complex `Order` objects in a clear, fluent way.

---

## Input and Output

**Program Output Example:**

```
=== Design Patterns Demo ===
Factory Method, Prototype, Builder

[Factory] Created pizza: L-size Margherita (basil, tomato, no extra cheese) -> $10.94

[Prototype] Original: L-size Margherita (basil, tomato, no extra cheese) -> $10.94
[Prototype] Clone   : L-size Margherita (basil, tomato, chili flakes, with extra cheese) -> $13.44

=== Order Summary ===
- L-size Margherita (basil, tomato, no extra cheese) -> $10.94
- L-size Margherita (basil, tomato, chili flakes, with extra cheese) -> $13.44

Total (after coupon): $21.94
Contactless Delivery: True
Note: Ring the bell twice
```

---

## Conclusion

This project demonstrates three creational design patterns that simplify and clarify object construction. The Factory Method centralizes object creation logic, making it easy to introduce new pizza types without modifying client code. The Prototype pattern allows objects to be duplicated and customized without risking unintended side effects. Finally, the Builder pattern separates the construction of an order from its representation, enabling a clear and fluent approach to assembling complex objects. Together, these patterns increase flexibility, readability, and maintainability in the codebase.