
from __future__ import annotations
from dataclasses import dataclass, field
from copy import deepcopy
from typing import List

@dataclass
class Pizza:
    name: str
    size: str  # 'S', 'M', 'L'
    base_price: float
    toppings: List[str] = field(default_factory=list)
    extra_cheese: bool = False

    def price(self) -> float:
        topping_cost = 0.75 * len(self.toppings)
        cheese_cost = 1.25 if self.extra_cheese else 0.0
        size_multiplier = {'S': 0.9, 'M': 1.0, 'L': 1.25}[self.size]
        return round((self.base_price + topping_cost + cheese_cost) * size_multiplier, 2)

    # --- Prototype pattern: provide a clone() that returns a deep copy ---
    def clone(self) -> 'Pizza':
        """Return a deep-copied clone so nested lists aren't shared."""
        return deepcopy(self)

    def describe(self) -> str:
        toppings = ', '.join(self.toppings) if self.toppings else 'no extra toppings'
        cheese = 'with extra cheese' if self.extra_cheese else 'no extra cheese'
        return f"{self.size}-size {self.name} ({toppings}, {cheese}) -> ${self.price()}"


# Concrete "prototype" presets
def margherita(size: str = 'M') -> Pizza:
    return Pizza(name='Margherita', size=size, base_price=7.50, toppings=['basil', 'tomato'])

def pepperoni(size: str = 'M') -> Pizza:
    return Pizza(name='Pepperoni', size=size, base_price=8.50, toppings=['pepperoni'])

def veggie(size: str = 'M') -> Pizza:
    return Pizza(name='Veggie', size=size, base_price=8.25, toppings=['mushroom', 'onion', 'olive'])
