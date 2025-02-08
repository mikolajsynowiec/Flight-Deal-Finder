import requests

SHEETY_PRICES_ENDPOINT = "https://api.sheety.co/cd6d5e7e706ead63ac81db724fbe4aef/copyOfFlightDeals/prices"

class DataManager:
    """Handles Sheety API requests to update and retrieve Google Sheet data."""

    def __init__(self):
        self.sheet_data = []

    def get_data(self):
        """Fetches the current sheet data from Sheety."""
        response = requests.get(SHEETY_PRICES_ENDPOINT)
        response.raise_for_status()
        self.sheet_data = response.json().get("prices", [])
        return self.sheet_data

    def update_price(self, row_id, new_price, departure_date, return_date, destination_city, destination_code):
        """Updates the Google Sheet with the lowest price, departure and return dates,
        and ensures the destination city and code are accurate.
        """
        url = f"{SHEETY_PRICES_ENDPOINT}/{row_id}"
        data = {
            "price": {
                "lowestPrice": new_price,
                "departureDate": departure_date,
                "returnDate": return_date,
                "destinationCity": destination_city,
                "destinationCode": destination_code
            }
        }
        response = requests.put(url, json=data)

        if response.status_code == 200:
            print(f"✅ Updated row {row_id} with new lowest price: ${new_price}, departure: {departure_date}, return: {return_date}")
        else:
            print(f"❌ Failed to update row {row_id}: {response.json()}")


