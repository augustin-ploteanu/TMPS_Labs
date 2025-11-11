from __future__ import annotations
from domain.factory import SimplePizzaFactory
from domain.models import Pizza, OrderBuilder
from domain.models import PrototypeRegistry

def main() -> None:
    print("=== Design Patterns Demo ===")
    print("Factory Method, Prototype, Builder\n")

    # Factory Method
    factory = SimplePizzaFactory()
    base = factory.create("margherita", size="L")
    print("[Factory] Created pizza:", base.describe())

    # Prototype
    registry = PrototypeRegistry()
    registry.register("base", base)

    # Clone using external prototype object
    spicy_clone = registry.clone("base")
    spicy_clone.toppings.append("chili flakes")
    spicy_clone.extra_cheese = True

    print("\n[Prototype] Original:", base.describe())
    print("[Prototype] Clone   :", spicy_clone.describe())

    # Builder
    order = (
        OrderBuilder("Ava Algorithm")
        .deliver_to("123 Binary Blvd")
        .add_pizza(base)
        .add_pizza(spicy_clone)
        .with_coupon(10)
        .with_note("Ring the bell twice")
        .contactless_delivery(True)
        .build()
    )

    print("\n=== Order Summary ===")
    for p in order.pizzas:
        print("-", p.describe())

    print(f"\nTotal (after coupon): ${order.total()}")
    print(f"Contactless Delivery: {order.contactless}")
    if order.note:
        print(f"Note: {order.note}")


if __name__ == "__main__":
    main()
