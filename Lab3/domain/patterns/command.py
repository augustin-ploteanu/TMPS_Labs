from abc import ABC, abstractmethod
from domain.models import Order, OrderStatus

class OrderCommand(ABC):
    @abstractmethod
    def execute(self):
        pass
    
    @abstractmethod
    def undo(self):
        pass

class ConfirmOrderCommand(OrderCommand):
    def __init__(self, order: Order, subject):
        self.order = order
        self.subject = subject
        self.previous_status = None
    
    def execute(self):
        self.previous_status = self.order.status
        self.order.status = OrderStatus.CONFIRMED
        self.order.calculate_total()
        self.subject.notify_observers(self.order)
        print(f"Order {self.order.order_id} confirmed")
    
    def undo(self):
        self.order.status = self.previous_status
        self.subject.notify_observers(self.order)  # Added notification
        print(f"Order {self.order.order_id} reverted to {self.previous_status.value}")

class ShipOrderCommand(OrderCommand):
    def __init__(self, order: Order, subject):
        self.order = order
        self.subject = subject
        self.previous_status = None
    
    def execute(self):
        if self.order.status != OrderStatus.CONFIRMED:
            raise ValueError("Order must be confirmed before shipping")
        
        self.previous_status = self.order.status
        self.order.status = OrderStatus.SHIPPED
        self.subject.notify_observers(self.order)
        print(f"Order {self.order.order_id} shipped")
    
    def undo(self):
        self.order.status = self.previous_status
        self.subject.notify_observers(self.order)  # Added notification
        print(f"Order {self.order.order_id} reverted to {self.previous_status.value}")

class CancelOrderCommand(OrderCommand):
    def __init__(self, order: Order, subject):
        self.order = order
        self.subject = subject
        self.previous_status = None
    
    def execute(self):
        self.previous_status = self.order.status
        self.order.status = OrderStatus.CANCELLED
        self.subject.notify_observers(self.order)
        print(f"Order {self.order.order_id} cancelled")
    
    def undo(self):
        self.order.status = self.previous_status
        self.subject.notify_observers(self.order)  # Added notification
        print(f"Order {self.order.order_id} reverted to {self.previous_status.value}")

class CommandInvoker:
    def __init__(self):
        self._history = []
    
    def execute_command(self, command: OrderCommand):
        command.execute()
        self._history.append(command)
    
    def undo_last(self):
        if self._history:
            command = self._history.pop()
            command.undo()