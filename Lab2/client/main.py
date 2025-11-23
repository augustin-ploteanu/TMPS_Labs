from domain.facade import ECommerceFacade
from domain.adapter import ModernPaymentSystem, ModernPaymentSystemInterface, PaymentAdapter
from domain.decorator import BasicOrderProcessor, ValidationDecorator, LoggingDecorator
from domain.models import OldPaymentProcessor, Order

def main():
    # Initialize the facade
    ecommerce = ECommerceFacade()
    
    # Display available products
    print("=== Available Products ===")
    for product in ecommerce.get_products():
        print(f"{product.id}: {product.name} - ${product.price:.2f}")
    
    # Create an order
    order = ecommerce.create_order("ORD-001")
    
    # Add items to order
    print("\n=== Adding Items to Order ===")
    try:
        order.add_item(ecommerce.find_product("1"), 1)  # Laptop
        order.add_item(ecommerce.find_product("2"), 2)  # Books
        order.add_item(ecommerce.find_product("3"), 1)  # Headphones
    except ValueError as e:
        print(f"Error: {e}")
        return
    
    print(order)
    
    # Process the complete order using facade
    ecommerce.process_complete_order(order)
    
    # Demonstrate individual patterns
    print("\n" + "="*50)
    print("DEMONSTRATING INDIVIDUAL PATTERNS")
    print("="*50)
    
    # Adapter pattern demonstration
    print("\n--- Adapter Pattern Demo ---")
    legacy_processor = OldPaymentProcessor()
    legacy_processor.process_payment_legacy(100.0, "USD")
    
    modern_system: ModernPaymentSystemInterface = ModernPaymentSystem()
    adapter = PaymentAdapter(modern_system)
    adapter.process_payment_legacy(100.0, "USD")
    
    # Decorator pattern demonstration
    print("\n--- Decorator Pattern Demo ---")
    test_order = ecommerce.create_order("TEST-001")
    
    # Without decorators
    print("\nBasic processor:")
    basic = BasicOrderProcessor()
    basic.process_order(test_order)
    
    # With decorators
    print("\nDecorated processor:")
    decorated = LoggingDecorator(ValidationDecorator(BasicOrderProcessor()))
    decorated.process_order(test_order)
    
    # Test with empty order (validation should fail)
    print("\n--- Testing Validation Decorator ---")
    empty_order = ecommerce.create_order("TEST-002")
    decorated.process_order(empty_order)

if __name__ == "__main__":
    main()