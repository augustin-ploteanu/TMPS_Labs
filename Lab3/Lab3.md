# **Lab 3: Behavioral Design Patterns**

## Theory

### **1. Chain of Responsibility**

The **Chain of Responsibility** pattern lets you pass requests along a chain of handlers. Upon receiving a request, each handler decides either to process the request or to pass it to the next handler in the chain. This pattern decouples the sender of a request from its receivers by giving multiple objects a chance to handle the request. The chain can be composed dynamically at runtime, and handlers can be added or removed flexibly. Common use cases include event handling systems, logging frameworks, and validation pipelines. However, there's no guarantee that a request will be handled unless the chain is properly configured.

---

### **2. Command**

The **Command** pattern turns a request into a stand-alone object that contains all information about the request. This transformation lets you pass requests as method arguments, delay or queue a request's execution, and support undoable operations. The pattern decouples the object that invokes the operation from the one that knows how to perform it, enabling features like command history, macro recording, and transactional behavior. Command objects can be stored, passed as parameters, and manipulated like any other object. The main disadvantage is the potential proliferation of command classes for each operation.

---

### **3. Iterator**

The **Iterator** pattern lets you traverse elements of a collection without exposing its underlying representation (list, stack, tree, etc.). It provides a standardized way to access elements sequentially regardless of the collection's internal structure. This pattern simplifies client code by providing a uniform interface for different collection types and supports multiple simultaneous traversals of the same collection. Iterators also help adhere to the Single Responsibility Principle by separating traversal algorithms from collection classes.

---

### **4. Mediator**

The **Mediator** pattern lets you reduce chaotic dependencies between objects. The pattern restricts direct communications between the objects and forces them to collaborate only via a mediator object. This promotes loose coupling by preventing objects from referring to each other explicitly, making the system easier to understand and maintain. The mediator encapsulates how objects interact, making it the sole component that knows about all other components. However, a mediator can become overly complex if it has to handle too many interactions.

---

### **5. Memento**

The **Memento** pattern lets you save and restore the previous state of an object without revealing the details of its implementation. It captures and externalizes an object's internal state so that the object can be restored to this state later, without violating encapsulation. The pattern involves three actors: the originator (creates mementos), the memento (stores state), and the caretaker (manages mementos). This is particularly useful for implementing undo mechanisms, but can be memory-intensive if states are large.

---

### **6. Observer**

The **Observer** pattern lets you define a subscription mechanism to notify multiple objects about any events that happen to the object they're observing. This pattern defines a one-to-many dependency between objects so that when one object changes state, all its dependents are notified and updated automatically. It promotes loose coupling between subjects and observers, making it easier to add new observers without modifying the subject. However, careless implementation can lead to memory leaks and unexpected update cascades.

---

### **7. State**

The **State** pattern lets an object alter its behavior when its internal state changes. It appears as if the object changed its class. The pattern organizes state-specific behaviors into separate classes and delegates state-dependent behavior to these classes. This eliminates the need for large conditional statements and makes state transitions explicit. The State pattern is particularly useful for objects that have complex, state-dependent behavior, but can lead to a proliferation of state classes.

---

### **8. Strategy**

The **Strategy** pattern lets you define a family of algorithms, put each of them into a separate class, and make their objects interchangeable. Strategy lets the algorithm vary independently from clients that use it. This pattern is particularly useful when you need different variants of an algorithm or when you have multiple similar classes that differ only in their behavior. By separating the behavior into strategy objects, you can comply with the Open/Closed Principle, allowing new strategies to be introduced without changing the context.

---

### **9. Template Method**

The **Template Method** pattern defines the skeleton of an algorithm in the superclass but lets subclasses override specific steps of the algorithm without changing its structure. The template method defines the sequence of steps in an algorithm, allowing subclasses to redefine certain steps without changing the algorithm's overall structure. This promotes code reuse and follows the Hollywood Principle ("Don't call us, we'll call you"). However, it can limit flexibility by enforcing a fixed algorithm structure.

---

### **10. Visitor**

The **Visitor** pattern lets you separate algorithms from the objects on which they operate. It allows you to add new operations to existing object structures without modifying the structures. The pattern involves a visitor interface with visit methods for each type of element, and concrete visitors that implement these operations. This makes it easy to add new operations but hard to add new element types. The Visitor pattern is particularly useful when you have many unrelated operations to perform on objects in a complex structure.

---

## Implementation

### **E-Commerce Order Processing System**

This project implements an e-commerce order processing system that demonstrates three behavioral design patterns working together to create a flexible and maintainable order management architecture.

---

### **1. Observer — Real-time Order Status Notifications**

`domain/patterns/observer.py`

```python
class OrderSubject:
    def __init__(self):
        self._observers: List[OrderObserver] = []
    
    def attach(self, observer: OrderObserver):
        if observer not in self._observers:
            self._observers.append(observer)
    
    def notify_observers(self, order: Order):
        for observer in self._observers:
            observer.update(order)

class EmailNotificationService(OrderObserver):
    def update(self, order: Order):
        print(f"[EMAIL] Order {order.order_id} status changed to {order.status.value}")
        if order.status == OrderStatus.CONFIRMED:
            print(f"[EMAIL] Order confirmed! Total: ${order.total_amount:.2f}")

class InventoryManagementService(OrderObserver):
    def update(self, order: Order):
        if order.status == OrderStatus.CONFIRMED:
            print(f"[INVENTORY] Updating stock for order {order.order_id}")
            for item in order.items:
                item.product.stock -= item.quantity
```

The Observer pattern enables real-time notifications across multiple services when order status changes. The `OrderSubject` maintains a list of observers (`EmailNotificationService`, `InventoryManagementService`, `AnalyticsService`) and automatically notifies them whenever an order's status is updated. This ensures that all concerned services stay synchronized without direct dependencies, promoting loose coupling and extensibility.

---

### **2. Strategy — Flexible Discount Calculation**

`domain/patterns/strategy.py`

```python
class DiscountStrategy(ABC):
    @abstractmethod
    def apply_discount(self, order: Order) -> float:
        pass

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
```

The Strategy pattern encapsulates different discount algorithms, making them interchangeable at runtime. The `DiscountContext` can switch between various discount strategies (`PercentageDiscountStrategy`, `FixedAmountDiscountStrategy`, `NoDiscountStrategy`) without modifying the order processing logic. This allows for flexible pricing policies and easy addition of new discount types while keeping the discount calculation logic separate from the main business logic.

---

### **3. Command — Undoable Order Operations**

`domain/patterns/command.py`

```python
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
        self.subject.notify_observers(self.order)

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
```

The Command pattern encapsulates order operations as objects, enabling features like undo functionality and command queuing. Concrete commands (`ConfirmOrderCommand`, `ShipOrderCommand`, `CancelOrderCommand`) encapsulate all information needed to perform and undo operations. The `CommandInvoker` maintains a history of executed commands, allowing users to undo operations and revert order status changes while maintaining system consistency through proper observer notifications.

---

## Input and Output

**Program Output Example:**

```
E-Commerce Order Processing System
==================================

=== Starting Order Processing ===

1. Original total: $1059.97
2. After 10% discount: $953.97
3. After $50 discount: $1009.97

4. Executing order commands:
[EMAIL] Order ORD001 status changed to confirmed
[EMAIL] Order confirmed! Total: $1059.97
[INVENTORY] Updating stock for order ORD001
[INVENTORY] Product Laptop stock updated to 9
[INVENTORY] Product Mouse stock updated to 48
[ANALYTICS] Recording order ORD001 with status confirmed
Order ORD001 confirmed
[EMAIL] Order ORD001 status changed to shipped
[EMAIL] Your order has been shipped!
[ANALYTICS] Recording order ORD001 with status shipped
Order ORD001 shipped

5. Undo last command:
[EMAIL] Order ORD001 status changed to confirmed
[EMAIL] Order confirmed! Total: $1059.97
[ANALYTICS] Recording order ORD001 with status confirmed
Order ORD001 reverted to confirmed

==================================
Order processing demonstration completed!
```

---

## Conclusion

This project successfully demonstrates three key behavioral design patterns working in harmony to create a robust e-commerce order processing system. The **Observer** pattern enables real-time coordination between different services, ensuring that email notifications, inventory updates, and analytics tracking happen automatically whenever order status changes. The **Strategy** pattern provides flexible discount calculation, allowing different pricing strategies to be applied interchangeably without modifying the core order processing logic. The **Command** pattern encapsulates order operations as objects, supporting undo functionality and maintaining a clear history of order state transitions.