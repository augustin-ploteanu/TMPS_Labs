from domain.models import Config, TripPlanBuilder, TripDirector
from domain.factory import CarFactory, BikeFactory


def demo_singleton():
    print("=== Singleton demo ===")
    c1 = Config()
    c2 = Config()
    print("Config 1:", c1)
    print("Config 2:", c2)
    print("Same object?", c1 is c2)
    # change once, seen everywhere
    c1.env = "production"
    print("Config 2 after change:", c2)
    print()


def demo_factory_method():
    print("=== Factory Method demo ===")
    car_factory = CarFactory()
    bike_factory = BikeFactory()

    car = car_factory.register_and_get_vehicle("Toyota")
    bike = bike_factory.register_and_get_vehicle("Trek")

    print(car.move())
    print(bike.move())
    print()


def demo_builder():
    print("=== Builder demo ===")
    builder = TripPlanBuilder()
    director = TripDirector(builder)

    city_trip = director.build_city_break()
    beach_trip = director.build_beach_holiday()

    print("City trip:", city_trip)
    print("Beach trip:", beach_trip)

    # also build manually
    custom_trip = (
        builder
        .set_destination("Chisinau")
        .set_vehicle("car")
        .set_hotel("local BnB")
        .add_activity("winery visit")
        .add_activity("city center walk")
        .build()
    )
    print("Custom trip:", custom_trip)
    print()


def main():
    demo_singleton()
    demo_factory_method()
    demo_builder()


if __name__ == "__main__":
    main()
