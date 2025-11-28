from abc import ABC, abstractmethod
from typing import List
from domain.models import Order, OrderStatus

class OrderObserver(ABC):
    @abstractmethod
    def update(self, order: Order):
        pass

class OrderSubject:
    def __init__(self):
        self._observers: List[OrderObserver] = []
    
    def attach(self, observer: OrderObserver):
        if observer not in self._observers:
            self._observers.append(observer)
    
    def detach(self, observer: OrderObserver):
        self._observers.remove(observer)
    
    def notify_observers(self, order: Order):
        for observer in self._observers:
            observer.update(order)

# Concrete Observers
class EmailNotificationService(OrderObserver):
    def update(self, order: Order):
        print(f"[EMAIL] Order {order.order_id} status changed to {order.status.value}")
        if order.status == OrderStatus.CONFIRMED:
            print(f"[EMAIL] Order confirmed! Total: ${order.total_amount:.2f}")
        elif order.status == OrderStatus.SHIPPED:
            print(f"[EMAIL] Your order has been shipped!")

class InventoryManagementService(OrderObserver):
    def __init__(self):
        self.processed_orders = set()  # Track which orders we've processed
    
    def update(self, order: Order):
        # Only process inventory when order is FIRST confirmed (not when reverting)
        if (order.status == OrderStatus.CONFIRMED and 
            order.order_id not in self.processed_orders):
            
            print(f"[INVENTORY] Updating stock for order {order.order_id}")
            for item in order.items:
                item.product.stock -= item.quantity
                print(f"[INVENTORY] Product {item.product.name} stock updated to {item.product.stock}")
            
            self.processed_orders.add(order.order_id)

class AnalyticsService(OrderObserver):
    def update(self, order: Order):
        print(f"[ANALYTICS] Recording order {order.order_id} with status {order.status.value}")
        if order.status == OrderStatus.DELIVERED:
            print(f"[ANALYTICS] Order {order.order_id} completed successfully!")