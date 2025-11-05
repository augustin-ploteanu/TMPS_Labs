
from __future__ import annotations
from typing import Protocol
from ..models.pizza import Pizza, margherita, pepperoni, veggie

class PizzaFactory(Protocol):
    def create(self, kind: str, size: str = 'M') -> Pizza:
        ...

class SimplePizzaFactory:
    """Factory Method: encapsulates the creation logic, returns a Pizza by 'kind'."""
    _registry = {
        'margherita': margherita,
        'pepperoni': pepperoni,
        'veggie': veggie,
    }

    def create(self, kind: str, size: str = 'M') -> Pizza:
        key = kind.strip().lower()
        ctor = self._registry.get(key)
        if not ctor:
            raise ValueError(f"Unknown pizza kind: {kind!r}. Known kinds: {sorted(self._registry)}")
        return ctor(size=size)
