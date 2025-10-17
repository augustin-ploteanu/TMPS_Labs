
# **Lab 0: SOLID Principles**

## Theory

SOLID principles are five object-oriented design guidelines that make software easier to maintain, scale, and understand. They are the following:

**Single Responsibility Principle:** A class should have only one reason to change, meaning it should focus on a single responsibility or purpose. This keeps code easier to understand, test, and maintain because each part does one well-defined job.

**Open/Closed Principle:** Software entities (classes, modules, functions) should be open for extension but closed for modification. In other words, you should be able to add new functionality without changing existing, stable code, typically by using interfaces or inheritance.

**Liskov Substitution Principle:** Objects of a superclass should be replaceable with objects of its subclasses without breaking the program’s behavior. This ensures consistent interfaces and prevents unexpected side effects when substituting implementations.
**Interface Segregation Principle:** Clients should not be forced to depend on interfaces they do not use. It promotes creating smaller, more specific interfaces instead of large, all-purpose ones.

**Dependency Inversion Principle:** High-level modules should depend on abstractions, not on low-level concrete implementations. This decouples components and makes it easier to change dependencies (like databases or APIs) without rewriting the core logic.

---

## Implementation

### SRP — `Cart` only manages items and totals

```python
class Cart:
    def __init__(self) -> None:
        self._items: List[CartItem] = []

    def add(self, product: Product, qty: int = 1) -> None:
        assert qty > 0
        self._items.append(CartItem(product, qty))

    @property
    def subtotal_cents(self) -> int:
        return sum(i.product.price_cents * i.qty for i in self._items)
```

`Cart` only manages cart data and subtotal logic. It doesn’t process payments or print receipts — one responsibility, one reason to change.

---

### OCP — Add new pricing rules without modifying existing logic

```python
PricingRule = Callable[[Cart], int]

def pct_off_over(threshold_cents: int, percent: float) -> PricingRule:
    def rule(cart: Cart) -> int:
        return int(cart.subtotal_cents * percent) if cart.subtotal_cents >= threshold_cents else 0
    return rule
```

New discount logic (like coupons or seasonal offers) can be added by defining new functions — the rest of the system remains unchanged.

---

### DIP — High-level logic depends on abstractions

```python
ChargeFn = Callable[[int], str]

class OrderService:
    def __init__(self, charge: ChargeFn, pricing_rules: Iterable[PricingRule]):
        self.charge = charge
        self.rules = list(pricing_rules)
```

`OrderService` depends on abstract callables (`ChargeFn`, `PricingRule`) instead of hard-coded payment processors. Dependencies (Stripe, PayPal, etc.) are injected at runtime.

---

## Input and Output

**User Input:**

* Enter product SKU and quantity (e.g., `COF 2`).
* Choose discounts (`y/N`).
* Select payment method (`1=Stripe`, `2=PayPal`).

**Program Output:**

```
=== RECEIPT ===
Subtotal: $17.97
Discount: -$1.80
TOTAL: $16.17
Transaction: stripe_txn_1617
```

---

## Conclusion

 This project demonstrates three of the SOLID principles: Single Responsibility, Open/Closed, and Dependency Inversion. Each class follows the SRP by having only one reason to change, for instance, the Cart handles items, pricing rules compute discounts, payment processors handle payments, and the receipt printer manages output rendering. The OCP principle is applied by allowing new pricing rules or payment processors to be added through new classes without altering existing code, ensuring the system is open for extension but closed for modification. Finally, the DIP principle is reflected in the design of the OrderService, which depends on abstractions, interfaces, rather than specific implementations, making the system more flexible and easily adaptable to different components.