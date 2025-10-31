from abc import ABC, abstractmethod
from domain.models.vehicles import Vehicle, Car, Bike


class VehicleFactory(ABC):
    """
    Factory Method base.
    Subclasses override create_vehicle to produce concrete products.
    """

    @abstractmethod
    def create_vehicle(self, brand: str) -> Vehicle:
        pass

    def register_and_get_vehicle(self, brand: str) -> Vehicle:
        """
        A 'template' style method:
        - create the vehicle
        - maybe log/register it
        - return it
        """
        vehicle = self.create_vehicle(brand)
        # here you could register to DB, log, etc.
        # print(f"Registered vehicle: {vehicle!r}")
        return vehicle


class CarFactory(VehicleFactory):
    def create_vehicle(self, brand: str) -> Vehicle:
        return Car(brand)


class BikeFactory(VehicleFactory):
    def create_vehicle(self, brand: str) -> Vehicle:
        return Bike(brand)
