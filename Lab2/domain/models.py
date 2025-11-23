from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List

@dataclass
class Product:
    id: str
    name: str
    price: float
    category: str

@dataclass
class OrderItem:
    product: Product
    quantity: int

class Order:
    def __init__(self, order_id: str):
        self.order_id = order_id
        self.items: List[OrderItem] = []
        self.total_amount = 0.0
        self.status = "Pending"
    
    def add_item(self, product: Product, quantity: int):
        self.items.append(OrderItem(product, quantity))
        self.total_amount += product.price * quantity
    
    def __str__(self):
        items_str = "\n".join([f"  - {item.product.name} x {item.quantity}: ${item.product.price * item.quantity:.2f}" 
                             for item in self.items])
        return f"Order {self.order_id} (Status: {self.status})\nItems:\n{items_str}\nTotal: ${self.total_amount:.2f}"

# Legacy system interface (Client Interface)
class LegacyPaymentSystem(ABC):
    @abstractmethod
    def process_payment_legacy(self, amount: float, currency: str) -> bool:
        pass

class OldPaymentProcessor(LegacyPaymentSystem):
    def process_payment_legacy(self, amount: float, currency: str) -> bool:
        print(f"Legacy: Processing {currency} {amount:.2f} via old system")
        return True