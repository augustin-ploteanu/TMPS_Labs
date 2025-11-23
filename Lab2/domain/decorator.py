from abc import ABC, abstractmethod
from .models import Order

# Component Interface
class OrderProcessor(ABC):
    @abstractmethod
    def process_order(self, order: Order) -> bool:
        pass

class BasicOrderProcessor(OrderProcessor):
    def process_order(self, order: Order) -> bool:
        print(f"Processing order {order.order_id}")
        order.status = "Processed"
        return True

# Base Decorator
class OrderProcessorDecorator(OrderProcessor):
    def __init__(self, processor: OrderProcessor):
        self._processor = processor
    
    def process_order(self, order: Order) -> bool:
        return self._processor.process_order(order)

# Concrete Decorators
class ValidationDecorator(OrderProcessorDecorator):
    def process_order(self, order: Order) -> bool:
        if not order.items:
            print("Validation failed: Order has no items")
            return False
        
        if order.total_amount <= 0:
            print("Validation failed: Invalid total amount")
            return False
        
        print("Order validation passed")
        return super().process_order(order)

class LoggingDecorator(OrderProcessorDecorator):
    def process_order(self, order: Order) -> bool:
        print(f"LOG: Starting to process order {order.order_id}")
        result = super().process_order(order)
        print(f"LOG: Order {order.order_id} processing {'completed' if result else 'failed'}")
        return result

class EmailNotificationDecorator(OrderProcessorDecorator):
    def process_order(self, order: Order) -> bool:
        result = super().process_order(order)
        if result:
            print(f"EMAIL: Order confirmation sent for order {order.order_id}")
        return result