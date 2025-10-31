from abc import ABC, abstractmethod


class Vehicle(ABC):
    @abstractmethod
    def move(self) -> str:
        """Return a string that represents the vehicle moving."""
        pass


class Car(Vehicle):
    def __init__(self, brand: str):
        self.brand = brand

    def move(self) -> str:
        return f"The car {self.brand} drives on the road."

    def __repr__(self):
        return f"Car(brand={self.brand!r})"


class Bike(Vehicle):
    def __init__(self, brand: str):
        self.brand = brand

    def move(self) -> str:
        return f"The bike {self.brand} rides on the road."

    def __repr__(self):
        return f"Bike(brand={self.brand!r})"
