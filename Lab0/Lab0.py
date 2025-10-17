from dataclasses import dataclass
from typing import Callable, Iterable, List

# --- SRP: Cart handles items and totals only ---
@dataclass(frozen=True)
class Product:
    sku: str
    name: str
    price_cents: int

@dataclass
class CartItem:
    product: Product
    qty: int

class Cart:
    def __init__(self) -> None:
        self._items: List[CartItem] = []

    def add(self, product: Product, qty: int = 1) -> None:
        assert qty > 0
        self._items.append(CartItem(product, qty))

    @property
    def subtotal_cents(self) -> int:
        return sum(i.product.price_cents * i.qty for i in self._items)

    @property
    def items(self) -> Iterable[CartItem]:
        return tuple(self._items)

# --- OCP: Pricing rules are pluggable callables ---
PricingRule = Callable[[Cart], int]

def pct_off_over(threshold_cents: int, percent: float) -> PricingRule:
    def rule(cart: Cart) -> int:
        return int(cart.subtotal_cents * percent) if cart.subtotal_cents >= threshold_cents else 0
    return rule

def buy_n_get_m_free(sku: str, n: int, m: int) -> PricingRule:
    def rule(cart: Cart) -> int:
        for ci in cart.items:
            if ci.product.sku == sku:
                groups = ci.qty // (n + m)
                return groups * m * ci.product.price_cents
        return 0
    return rule

# --- DIP: OrderService depends on abstractions (callables) ---
ChargeFn = Callable[[int], str]

class OrderService:
    def __init__(self, charge: ChargeFn, pricing_rules: Iterable[PricingRule]):
        self.charge = charge
        self.rules = list(pricing_rules)

    def checkout(self, cart: Cart) -> str:
        subtotal = cart.subtotal_cents
        discount = sum(r(cart) for r in self.rules)
        total = max(subtotal - discount, 0)
        txn_id = self.charge(total)
        return f"Subtotal: ${subtotal/100:.2f}\nDiscount: -${discount/100:.2f}\nTOTAL: ${total/100:.2f}\nTransaction: {txn_id}"

# --- Concrete dependencies ---
def stripe_charge(amount_cents: int) -> str:
    if amount_cents <= 0: raise ValueError("Amount must be positive")
    return f"stripe_txn_{amount_cents}"

def paypal_charge(amount_cents: int) -> str:
    if amount_cents <= 0: raise ValueError("Amount must be positive")
    return f"paypal_txn_{amount_cents}"

# --- Interactive CLI ---
if __name__ == "__main__":
    catalog = {
        "COF": Product("COF", "Coffee", 599),
        "TEA": Product("TEA", "Tea", 399),
        "CAC": Product("CAC", "Cocoa", 499),
    }

    cart = Cart()
    print("Available products:")
    for sku, p in catalog.items():
        print(f"{sku}: {p.name} - ${p.price_cents/100:.2f}")

    while True:
        line = input("Add item (SKU qty) or blank to finish: ").strip()
        if not line: break
        try:
            sku, qty_str = line.split()
            cart.add(catalog[sku.upper()], int(qty_str))
        except Exception:
            print("Invalid input. Try again.")
    if not cart.items:
        print("Cart empty. Exiting.")
        exit()

    # choose pricing rules
    rules = []
    if input("Apply 10% off over $20? (y/N): ").strip().lower() == "y":
        rules.append(pct_off_over(2000, 0.10))
    if input("Apply 'buy 2 get 1 free' for Coffee? (y/N): ").strip().lower() == "y":
        rules.append(buy_n_get_m_free("COF", 2, 1))

    # choose processor
    choice = input("Choose payment processor (1=Stripe, 2=PayPal): ").strip()
    charge_fn = stripe_charge if choice == "1" else paypal_charge

    service = OrderService(charge_fn, rules)
    print("\n=== RECEIPT ===")
    print(service.checkout(cart))
