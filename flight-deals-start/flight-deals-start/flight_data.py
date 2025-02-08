class FlightData:
    """Structures flight information to be processed and stored."""

    def __init__(self, origin, destination, price, departure_date, return_date):
        self.origin = origin
        self.destination = destination
        self.price = price
        self.departure_date = departure_date
        self.return_date = return_date

    def __str__(self):
        return (f"Departure: {self.origin} → Destination: {self.destination}\n"
                f"Departure Date: {self.departure_date}\n"
                f"Return Date: {self.return_date}\n"
                f"Price: ${self.price}")
