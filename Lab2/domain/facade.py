from .models import Order, Product, OldPaymentProcessor
from .adapter import ModernPaymentSystem, ModernPaymentSystemInterface, PaymentAdapter
from .decorator import BasicOrderProcessor, ValidationDecorator, LoggingDecorator, EmailNotificationDecorator

class ECommerceFacade:
    """Facade that simplifies the complex e-commerce system"""
    
    def __init__(self):
        self.products = [
            Product("1", "Laptop", 999.99, "Electronics"),
            Product("2", "Book", 19.99, "Education"),
            Product("3", "Headphones", 149.99, "Electronics")
        ]
        
        # Set up the decorated order processor
        basic_processor = BasicOrderProcessor()
        decorated_processor = EmailNotificationDecorator(
            LoggingDecorator(
                ValidationDecorator(basic_processor)
            )
        )
        self.order_processor = decorated_processor
        
        # Set up payment system with adapter
        self.modern_payment_system: ModernPaymentSystemInterface = ModernPaymentSystem()
        self.payment_adapter = PaymentAdapter(self.modern_payment_system)
    
    def get_products(self) -> list:
        return self.products
    
    def create_order(self, order_id: str) -> Order:
        return Order(order_id)
    
    def find_product(self, product_id: str) -> Product:
        for product in self.products:
            if product.id == product_id:
                return product
        raise ValueError(f"Product {product_id} not found")
    
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