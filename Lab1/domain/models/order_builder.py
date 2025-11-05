
from __future__ import annotations
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
        discount = subtotal * (self.coupon_pct / 100.0)
        return round(subtotal - discount, 2)

class OrderBuilder:
    """Fluent Builder for Order objects."""
    def __init__(self, customer: str):
        self._customer = customer
        self._address: Optional[str] = None
        self._pizzas: List[Pizza] = []
        self._note: Optional[str] = None
        self._coupon_pct: float = 0.0
        self._contactless: bool = False

    def deliver_to(self, address: str) -> 'OrderBuilder':
        self._address = address
        return self

    def add_pizza(self, pizza: Pizza) -> 'OrderBuilder':
        self._pizzas.append(pizza)
        return self

    def with_note(self, note: str) -> 'OrderBuilder':
        self._note = note
        return self

    def with_coupon(self, pct: float) -> 'OrderBuilder':
        self._coupon_pct = max(0.0, min(100.0, pct))
        return self

    def contactless_delivery(self, enabled: bool = True) -> 'OrderBuilder':
        self._contactless = enabled
        return self

    def build(self) -> Order:
        return Order(
            customer=self._customer,
            address=self._address,
            pizzas=list(self._pizzas),
            note=self._note,
            coupon_pct=self._coupon_pct,
            contactless=self._contactless,
        )
