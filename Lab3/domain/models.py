from dataclasses import dataclass
from typing import List
from enum import Enum

class OrderStatus(Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"

@dataclass
class Product:
    id: str
    name: str
    price: float
    stock: int

@dataclass
class OrderItem:
    product: Product
    quantity: int

@dataclass
class Order:
    order_id: str
    items: List[OrderItem]
    status: OrderStatus
    total_amount: float = 0.0
    
    def calculate_total(self):
        self.total_amount = sum(item.product.price * item.quantity for item in self.items)
        return self.total_amount