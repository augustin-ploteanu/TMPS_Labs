from abc import ABC, abstractmethod
from domain.models import Order

class DiscountStrategy(ABC):
    @abstractmethod
    def apply_discount(self, order: Order) -> float:
        pass

class NoDiscountStrategy(DiscountStrategy):
    def apply_discount(self, order: Order) -> float:
        return order.calculate_total()

class PercentageDiscountStrategy(DiscountStrategy):
    def __init__(self, percentage: float):
        self.percentage = percentage
    
    def apply_discount(self, order: Order) -> float:
        total = order.calculate_total()
        discount = total * (self.percentage / 100)
        return total - discount

class FixedAmountDiscountStrategy(DiscountStrategy):
    def __init__(self, amount: float):
        self.amount = amount
    
    def apply_discount(self, order: Order) -> float:
        total = order.calculate_total()
        return max(0, total - self.amount)

class DiscountContext:
    def __init__(self, strategy: DiscountStrategy = None):
        self._strategy = strategy or NoDiscountStrategy()
    
    def set_strategy(self, strategy: DiscountStrategy):
        self._strategy = strategy
    
    def calculate_final_amount(self, order: Order) -> float:
        return self._strategy.apply_discount(order)