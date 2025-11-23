from abc import ABC, abstractmethod
from .models import LegacyPaymentSystem, Order

# Service Interface
class ModernPaymentSystemInterface(ABC):
    @abstractmethod
    def process_payment(self, order: Order, payment_method: str) -> bool:
        pass

class ModernPaymentSystem(ModernPaymentSystemInterface):
    """Modern payment system with different interface"""
    def process_payment(self, order: Order, payment_method: str) -> bool:
        print(f"Modern: Processing ${order.total_amount:.2f} via {payment_method}")
        return True

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