from domain.services import OrderProcessingService

def main():
    print("E-Commerce Order Processing System")
    print("==================================\n")
    
    # Initialize the order processing service
    order_processor = OrderProcessingService()
    
    # Create a sample order
    order = order_processor.create_sample_order()
    
    # Process the order workflow
    order_processor.process_order_workflow(order)
    
    print("\n==================================")
    print("Order processing demonstration completed!")

if __name__ == "__main__":
    main()