# **Lab 1: Creational Design Patterns**

## Theory

### **1. Singleton**

The **Singleton** pattern ensures that a class has only one instance throughout the application and provides a single, global access point to it. It’s commonly used for shared resources like configuration managers, loggers, or database connections. The pattern controls object creation internally, ensuring all code refers to the same instance, which simplifies global state management but can make testing and dependency management more difficult if overused.

### **2. Builder**

The **Builder** pattern separates the construction of a complex object from its representation, allowing the same construction process to produce different variations of the object. It’s useful when creating objects that require multiple steps or configurations, making code cleaner and more flexible. By encapsulating object assembly logic, the builder avoids long constructors and improves readability and reusability.

### **3. Prototype**

The **Prototype** pattern creates new objects by cloning existing ones instead of constructing them from scratch. It’s ideal when object creation is resource-intensive or involves complex initialization. By copying a pre-existing prototype, this pattern enables efficient object creation and dynamic configuration, though it requires careful handling of deep versus shallow copies to prevent unintended side effects.

### **4. Object Pooling**

The **Object Pooling** pattern maintains a set of initialized, reusable objects instead of creating and destroying them repeatedly. When a client needs an object, it borrows one from the pool, and when done, it returns it for reuse. This approach significantly improves performance in systems where object creation is expensive, such as in database or network connections, but requires careful management to avoid concurrency issues or resource leaks.

### **5. Factory Method**

The **Factory Method** pattern defines an interface for creating objects but lets subclasses decide which specific class to instantiate. It encapsulates object creation logic, allowing new product types to be added without modifying existing code. This promotes flexibility, extensibility, and adherence to the Open/Closed Principle, making it ideal for frameworks or libraries that must create objects without knowing their exact types in advance.

### **6. Abstract Factory**

The **Abstract Factory** pattern provides an interface for creating families of related or dependent objects without specifying their concrete classes. It’s used when a system must be independent of how its objects are created, composed, or represented. By grouping related factories together, it ensures consistency among created products and simplifies switching between different configurations or environments, such as different UI themes or database backends.


---

## Implementation

The project demonstrates all three patterns in a small **travel planning system**.

### Folder Structure

```
Lab1/
├── client/
│   └── main.py
└── domain/
    ├── factory/
    │   ├── __init__.py
    │   └── vehicle_factory.py
    ├── models/
    │   ├── __init__.py
    │   ├── config.py
    │   ├── trip_builder.py
    │   └── vehicles.py
```

---

### **1. Singleton — `Config`**

```python
# domain/models/config.py
class Config:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.env = "dev"
            cls._instance.debug = True
        return cls._instance
```

**Explanation:**

* The `Config` class restricts instantiation to a single object.
* Any new variable access (`Config()`) returns the same instance.
* Used to hold global environment settings (`env`, `debug`).

**Example Output:**

```
Config 1: <Config env='dev' debug=True>
Config 2: <Config env='dev' debug=True>
Same object? True
```

---

### **2. Builder — `TripPlanBuilder` and `TripDirector`**

```python
# domain/models/trip_builder.py
class TripPlanBuilder:
    def __init__(self):
        self.reset()

    def reset(self):
        self._destination = None
        self._vehicle = None
        self._hotel = None
        self._activities = []
        return self

    def set_destination(self, destination: str):
        self._destination = destination
        return self

    def set_vehicle(self, vehicle: str):
        self._vehicle = vehicle
        return self

    def set_hotel(self, hotel: str):
        self._hotel = hotel
        return self

    def add_activity(self, activity: str):
        self._activities.append(activity)
        return self

    def build(self) -> "TripPlan":
        if not self._destination:
            raise ValueError("Destination is required")
        return TripPlan(
            destination=self._destination,
            vehicle=self._vehicle or "bus",
            hotel=self._hotel or "standard guest house",
            activities=self._activities or ["city walk"]
        )
```

**Explanation:**

* The **builder** constructs a `TripPlan` step-by-step.
* `TripDirector` provides ready-made travel templates (e.g., `build_city_break`, `build_beach_holiday`).
* Encourages **flexibility** in building custom trip configurations.

**Example Output:**

```
City trip: TripPlan(destination='Paris', vehicle='train', hotel='4-star city hotel', activities=['museum', 'restaurant'])
Beach trip: TripPlan(destination='Malta', vehicle='plane', hotel='seaside resort', activities=['beach', 'boat tour'])
```

---

### **3. Factory Method — `VehicleFactory`**

```python
# domain/factory/vehicle_factory.py
class VehicleFactory(ABC):
    @abstractmethod
    def create_vehicle(self, brand: str) -> Vehicle:
        pass

    def register_and_get_vehicle(self, brand: str) -> Vehicle:
        vehicle = self.create_vehicle(brand)
        return vehicle


class CarFactory(VehicleFactory):
    def create_vehicle(self, brand: str) -> Vehicle:
        return Car(brand)


class BikeFactory(VehicleFactory):
    def create_vehicle(self, brand: str) -> Vehicle:
        return Bike(brand)
```

**Explanation:**

* The `VehicleFactory` defines an interface for creating a vehicle.
* Concrete factories (`CarFactory`, `BikeFactory`) override `create_vehicle` to return specific vehicle types.
* The client depends only on the factory interface, not concrete implementations — ensuring **loose coupling**.

**Example Output:**

```
The car Toyota drives on the road.
The bike Trek rides on the road.
```

---

### **Client Demo**

```python
# client/main.py
def main():
    demo_singleton()
    demo_factory_method()
    demo_builder()
```

**Execution:**

```bash
python -m client.main
```

**Output Summary:**

```
=== Singleton demo ===
Same object? True

=== Factory Method demo ===
The car Toyota drives on the road.
The bike Trek rides on the road.

=== Builder demo ===
City trip: TripPlan(destination='Paris', ...)
Beach trip: TripPlan(destination='Malta', ...)
Custom trip: TripPlan(destination='London', ...)
```

---

## Conclusion

This laboratory work demonstrates the application of three creational design patterns—Singleton, Builder, and Factory Method—within a  modular project. The Singleton pattern ensures a single global configuration instance for consistent state management, the Builder pattern simplifies the step-by-step creation of complex objects like travel plans while maintaining flexibility, and the Factory Method pattern decouples object creation from usage, promoting scalability and adherence to the Open/Closed Principle. Together, these patterns illustrate how structured design approaches can improve code reusability, maintainability, and clarity, resulting in software that is both modular and easily extensible for future growth.
