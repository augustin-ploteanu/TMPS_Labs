# **Lab 2: Structural Design Patterns**

## Theory

### **1. Adapter**

The **Adapter** pattern converts the interface of one class into another interface that the client expects. It is commonly used when integrating incompatible components, legacy classes, or third-party libraries without modifying their source code. By wrapping an object with an adapter, the client interacts with it through a consistent interface, enabling interoperability and simplifying integration. While adapters provide flexibility, overuse may complicate the system by introducing additional layers of abstraction.

---

### **2. Bridge**

The **Bridge** pattern decouples an abstraction from its implementation so the two can vary independently. Instead of binding an abstraction to a specific implementation at compile time, the bridge separates them into parallel class hierarchies connected via composition. This allows new abstractions and new implementations to be added without modifying existing code, making the pattern ideal for platforms that require extensibility, such as GUI frameworks or device drivers. However, using Bridge unnecessarily may increase structural complexity.

---

### **3. Composite**

The **Composite** pattern organizes objects into tree structures, allowing individual objects and groups of objects to be treated uniformly. Both leaf objects and composite objects share the same interface, enabling recursive operations over hierarchical structures such as file systems, menus, or graphic components. This pattern simplifies client code and enhances flexibility, though it may obscure differences between simple and complex elements if not carefully documented.

---

### **4. Decorator**

The **Decorator** pattern allows behavior to be added dynamically to individual objects without modifying their classes. By wrapping an object with one or more decorators, new responsibilities can be layered at runtime, supporting flexible extension and avoiding the need for large subclasses. This is useful in scenarios such as formatting streams, GUI element enhancements, or optional features. While powerful, nested decorators can become difficult to trace and debug if overused.

---

### **5. Facade**

The **Facade** pattern provides a simplified, high-level interface to a complex subsystem. Instead of exposing many components and detailed operations directly to the client, a facade bundles common workflows into a small set of easy-to-call methods. This reduces coupling, improves readability, and separates high-level orchestration from low-level implementation. However, if the subsystem evolves significantly, the facade may require updates to maintain functionality.

---

### **6. Flyweight**

The **Flyweight** pattern reduces memory usage by sharing large numbers of fine-grained objects that have identical or similar intrinsic data. External, variable state is stored outside the flyweight and passed in during operations, while intrinsic, immutable state is shared. This pattern is effective in contexts like rendering text characters, particles in simulations, or objects in large collections. While it improves efficiency, it introduces complexity by separating shared and external state, requiring careful design to avoid inconsistencies.

---

### **7. Proxy**

The **Proxy** pattern provides a stand-in object that controls access to another object. Proxies can perform tasks such as lazy initialization, access control, caching, logging, or remote communication before delegating operations to the underlying real object. This allows clients to use the proxy just like the real object while benefiting from additional functionality or reduced resource usage. However, proxies may introduce performance overhead or obscure the true cost of operations.

---

## Implementation

### **E-Commerce Order Processing System**

This project implements an e-commerce order processing system that demonstrates three structural design patterns working together to create a flexible and maintainable architecture.

---

### **1. Adapter — Integrating Legacy Payment System**

`adapter.py`

```python
class PaymentAdapter(LegacyPaymentSystem):
    """Adapter that makes ModernPaymentSystem compatible with LegacyPaymentSystem"""
    def __init__(self, modern_system: ModernPaymentSystemInterface):
        self.modern_system = modern_system
    
    def process_payment_legacy(self, amount: float, currency: str) -> bool:
        # Create a temporary order to adapt to modern system
        temp_order = Order("temp")
        temp_order.total_amount = amount
        
        # Convert legacy parameters to modern format
        payment_method = "credit_card"  # Default for legacy system
        
        return self.modern_system.process_payment(temp_order, payment_method)
```

The Adapter pattern allows the system to use a modern payment system with a legacy payment interface. The `PaymentAdapter` converts the legacy method call `process_payment_legacy(amount, currency)` into the modern system's expected format `process_payment(order, payment_method)`. This enables seamless integration without modifying either system's code.

---

### **2. Decorator — Enhancing Order Processing**

`decorator.py`

```python
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
```

The Decorator pattern dynamically adds responsibilities to order processing without modifying the core `BasicOrderProcessor`. Multiple decorators can be stacked:
- **ValidationDecorator**: Ensures orders have valid items and amounts
- **LoggingDecorator**: Adds audit trail for order processing
- **EmailNotificationDecorator**: Sends confirmation emails

This allows flexible combination of features and follows the Open/Closed Principle.

---

### **3. Facade — Simplified E-Commerce Interface**

`facade.py`

```python
class ECommerceFacade:
    """Facade that simplifies the complex e-commerce system"""
    
    def process_complete_order(self, order: Order) -> bool:
        """Facade method that handles the entire order process"""
        print(f"\n=== Processing Complete Order: {order.order_id} ===")
        
        # Process order with all decorators
        if not self.order_processor.process_order(order):
            return False
        
        # Process payment using adapter
        if not self.payment_adapter.process_payment_legacy(order.total_amount, "USD"):
            print("Payment failed")
            return False
        
        print(f"=== Order {order.order_id} completed successfully ===")
        return True
```

The Facade pattern provides a simple interface to the complex e-commerce subsystem. The `ECommerceFacade` coordinates multiple components:
- Product catalog management
- Decorated order processing pipeline
- Adapted payment system integration

Clients can process complete orders with a single method call, hiding the complexity of the underlying interactions.

---

## Input and Output

**Program Output Example:**

```
=== Available Products ===
1: Laptop - $999.99
2: Book - $19.99
3: Headphones - $149.99

=== Adding Items to Order ===
Order ORD-001 (Status: Pending)
Items:
  - Laptop x 1: $999.99
  - Book x 2: $39.98
  - Headphones x 1: $149.99
Total: $1189.96

=== Processing Complete Order: ORD-001 ===
LOG: Starting to process order ORD-001
Order validation passed
Processing order ORD-001
LOG: Order ORD-001 processing completed
EMAIL: Order confirmation sent for order ORD-001
Modern: Processing $1189.96 via credit_card
=== Order ORD-001 completed successfully ===

==================================================
DEMONSTRATING INDIVIDUAL PATTERNS
==================================================

--- Adapter Pattern Demo ---
Legacy: Processing USD 100.00 via old system
Modern: Processing $100.00 via credit_card

--- Decorator Pattern Demo ---

Basic processor:
Processing order TEST-001

Decorated processor:
LOG: Starting to process order TEST-001
Validation failed: Order has no items
LOG: Order TEST-001 processing failed

--- Testing Validation Decorator ---
LOG: Starting to process order TEST-002
Validation failed: Order has no items
LOG: Order TEST-002 processing failed
```

---

## Conclusion

This project demonstrates three key structural design patterns that work together to create a robust e-commerce system. The **Adapter** pattern seamlessly integrates incompatible payment systems, allowing legacy and modern components to coexist. The **Decorator** pattern enables dynamic addition of cross-cutting concerns like validation, logging, and notifications without modifying core business logic. The **Facade** pattern provides a simplified interface that orchestrates complex subsystem interactions, making the system easier to use and maintain.

Together, these patterns create a flexible architecture where:
- New payment systems can be integrated via adapters
- Additional order processing features can be added through decorators
- Complex workflows are hidden behind simple facade methods

This approach results in a system that is both extensible and maintainable, following key software design principles such as Separation of Concerns and the Open/Closed Principle.