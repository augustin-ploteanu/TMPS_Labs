class TripPlan:
    def __init__(self, destination: str, vehicle: str, hotel: str, activities: list[str]):
        self.destination = destination
        self.vehicle = vehicle
        self.hotel = hotel
        self.activities = activities

    def __repr__(self):
        return (
            f"TripPlan(destination={self.destination!r}, "
            f"vehicle={self.vehicle!r}, hotel={self.hotel!r}, "
            f"activities={self.activities!r})"
        )


class TripPlanBuilder:
    """
    Builder that knows how to create a TripPlan piece by piece.
    """

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

    def build(self) -> TripPlan:
        if not self._destination:
            raise ValueError("Destination is required")
        # fill in defaults if missing
        vehicle = self._vehicle or "bus"
        hotel = self._hotel or "standard guest house"
        activities = self._activities or ["city walk"]
        trip = TripPlan(
            destination=self._destination,
            vehicle=vehicle,
            hotel=hotel,
            activities=activities,
        )
        # optional: reset for reuse
        self.reset()
        return trip


class TripDirector:
    """
    Director: optional helper that defines common building recipes.
    You don't have to use it, but it shows the pattern more clearly.
    """

    def __init__(self, builder: TripPlanBuilder):
        self.builder = builder

    def build_city_break(self) -> TripPlan:
        return (
            self.builder
            .set_destination("Paris")
            .set_vehicle("train")
            .set_hotel("4-star city hotel")
            .add_activity("museum")
            .add_activity("restaurant")
            .build()
        )

    def build_beach_holiday(self) -> TripPlan:
        return (
            self.builder
            .set_destination("Malta")
            .set_vehicle("plane")
            .set_hotel("seaside resort")
            .add_activity("beach")
            .add_activity("boat tour")
            .build()
        )
