from __future__ import annotations
from copy import deepcopy
from typing import Dict
from .pizza import Pizza

class PrototypeRegistry:
    """External Prototype Manager."""
    def __init__(self):
        self._registry: Dict[str, Pizza] = {}

    def register(self, key: str, pizza: Pizza) -> None:
        self._registry[key.lower()] = pizza

    def clone(self, key: str) -> Pizza:
        try:
            return deepcopy(self._registry[key.lower()])
        except KeyError:
            raise ValueError(f"No prototype registered under '{key}'")
