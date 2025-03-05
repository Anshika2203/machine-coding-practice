import uuid

class Driver:
    def __init__(self, driver_id, name, location):
        self.driver_id = driver_id
        self.name = name
        self.location = location
        self.available = True

class Rider:
    def __init__(self, rider_id, name, location):
        self.rider_id = rider_id
        self.name = name
        self.location = location

class CabBooking:
    def __init__(self):
        self.drivers = {}
        self.riders = {}
        self.rides = {}

    def add_driver(self, driver_id, name, location):
        if driver_id in self.drivers:
            raise ValueError("Driver ID already exists.")
        self.drivers[driver_id] = Driver(driver_id, name, location)

    def add_rider(self, rider_id, name, location):
        if rider_id in self.riders:
            raise ValueError("Rider ID already exists.")
        self.riders[rider_id] = Rider(rider_id, name, location)

    def update_location(self, user_id, new_location, user_type):
        if user_type == "driver" and user_id in self.drivers:
            self.drivers[user_id].location = new_location
        elif user_type == "rider" and user_id in self.riders:
            self.riders[user_id].location = new_location
        else:
            raise ValueError("User not found.")

    def find_ride(self, rider_id):
        if rider_id not in self.riders:
            raise ValueError("Rider not found.")
        rider = self.riders[rider_id]
        available_drivers = [d for d in self.drivers.values() if d.available]
        if not available_drivers:
            return "No drivers available."
        return min(available_drivers, key=lambda d: abs(d.location - rider.location)).driver_id

    def book_ride(self, rider_id):
        driver_id = self.find_ride(rider_id)
        if isinstance(driver_id, str):
            return driver_id  # No driver available
        self.drivers[driver_id].available = False
        ride_id = str(uuid.uuid4())
        self.rides[ride_id] = {"rider_id": rider_id, "driver_id": driver_id, "fare": None}
        return ride_id

    def calculate_bill(self, ride_id, distance, rate_per_km=10):
        if ride_id not in self.rides:
            raise ValueError("Ride not found.")
        fare = distance * rate_per_km
        self.rides[ride_id]["fare"] = fare
        self.drivers[self.rides[ride_id]["driver_id"].available] = True  # Free driver after ride
        return fare


if __name__ == "__main__":
    cab_system = CabBooking()
    cab_system.add_driver("D1", "Alice", 10)
    cab_system.add_driver("D2", "Bob", 5)
    cab_system.add_rider("R1", "Charlie", 8)
    
    ride_id = cab_system.book_ride("R1")
    if "No drivers available" not in ride_id:
        print("Ride booked! Ride ID:", ride_id)
        fare = cab_system.calculate_bill(ride_id, 15)
        print("Total Fare:", fare)
    else:
        print(ride_id)

# mistake in fare and getting driver id from available drivers