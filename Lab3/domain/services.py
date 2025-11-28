from domain.patterns.observer import OrderSubject, EmailNotificationService, InventoryManagementService, AnalyticsService
from domain.patterns.strategy import DiscountContext, PercentageDiscountStrategy, FixedAmountDiscountStrategy
from domain.patterns.command import CommandInvoker, ConfirmOrderCommand, ShipOrderCommand, CancelOrderCommand
from domain.models import Order, Product, OrderItem, OrderStatus  # Added OrderStatus import

class OrderProcessingService:
    def __init__(self):
        self.order_subject = OrderSubject()
        self.command_invoker = CommandInvoker()
        
        # Attach observers
        self.order_subject.attach(EmailNotificationService())
        self.order_subject.attach(InventoryManagementService())
        self.order_subject.attach(AnalyticsService())
    
    def create_sample_products(self):
        return [
            Product("P001", "Laptop", 999.99, 10),
            Product("P002", "Mouse", 29.99, 50),
            Product("P003", "Keyboard", 79.99, 30)
        ]
    
    def create_sample_order(self):
        products = self.create_sample_products()
        order_items = [
            OrderItem(products[0], 1),
            OrderItem(products[1], 2)
        ]
        return Order("ORD001", order_items, OrderStatus.PENDING)
    
    def process_order_workflow(self, order: Order):
        print("=== Starting Order Processing ===")
        
        # Strategy Pattern: Apply discounts
        discount_context = DiscountContext()
        
        print(f"\n1. Original total: ${order.calculate_total():.2f}")
        
        # Apply 10% discount
        discount_context.set_strategy(PercentageDiscountStrategy(10))
        final_amount = discount_context.calculate_final_amount(order)
        print(f"2. After 10% discount: ${final_amount:.2f}")
        
        # Apply fixed amount discount
        discount_context.set_strategy(FixedAmountDiscountStrategy(50))
        final_amount = discount_context.calculate_final_amount(order)
        print(f"3. After $50 discount: ${final_amount:.2f}")
        
        # Command Pattern: Execute order workflow
        print("\n4. Executing order commands:")
        confirm_cmd = ConfirmOrderCommand(order, self.order_subject)
        ship_cmd = ShipOrderCommand(order, self.order_subject)
        
        self.command_invoker.execute_command(confirm_cmd)
        self.command_invoker.execute_command(ship_cmd)
        
        # Demonstrate undo
        print("\n5. Undo last command:")
        self.command_invoker.undo_last()