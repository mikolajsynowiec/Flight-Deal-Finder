import requests
import time


class FlightSearch:
    """Handles flight search using Amadeus API."""

    API_URL = "https://test.api.amadeus.com"

    def __init__(self, api_key, api_secret):
        self.api_key = api_key
        self.api_secret = api_secret
        self.token = None
        self.token_expiry = 0
        self.get_access_token()

    def get_access_token(self):
        """Authenticate with Amadeus API and get an access token."""
        url = f"{self.API_URL}/v1/security/oauth2/token"
        data = {
            "grant_type": "client_credentials",
            "client_id": self.api_key,
            "client_secret": self.api_secret
        }

        response = requests.post(url, data=data)
        response.raise_for_status()
        result = response.json()
        self.token = result["access_token"]
        self.token_expiry = time.time() + result["expires_in"] - 60

    def check_token(self):
        """Ensure token is valid before making a request."""
        if time.time() >= self.token_expiry:
            self.get_access_token()

    def parse_duration(self, duration_str):
        """
        Parses ISO 8601 duration format (e.g., 'PT10H30M') into total minutes.
        """
        duration_str = duration_str.replace("PT", "").upper()
        hours, minutes = 0, 0

        if "H" in duration_str:
            hours, duration_str = duration_str.split("H")
            hours = int(hours)

        if "M" in duration_str:
            minutes = int(duration_str.replace("M", ""))

        return (hours * 60) + minutes

    def search_cheapest_round_trip(self, origin, destination, departure_date, return_date):
        """Search for the cheapest round-trip flight while applying filters."""
        self.check_token()
        url = f"{self.API_URL}/v2/shopping/flight-offers"
        headers = {"Authorization": f"Bearer {self.token}"}
        params = {
            "originLocationCode": origin,
            "destinationLocationCode": destination,
            "departureDate": departure_date,
            "returnDate": return_date,
            "adults": 1,
            "currencyCode": "USD",
            "max": 5  # Get multiple offers to find a valid one
        }

        response = requests.get(url, headers=headers, params=params)
        if response.status_code != 200 or not response.json().get("data"):
            return None

        flights = response.json()["data"]

        # Filter flights that meet criteria
        for flight in flights:
            itineraries = flight["itineraries"]

            # Check outbound and return journeys
            for itinerary in itineraries:
                duration = self.parse_duration(itinerary["duration"])
                stops = len(itinerary["segments"]) - 1

                # Ensure flight duration is under 24 hours (1440 minutes) and stops <= 3
                if duration <= 1440 and stops <= 3:
                    return flight  # Return the first valid flight

        return None  # No valid flights found
