from datetime import datetime, timedelta
from data_manager import DataManager
from flight_search import FlightSearch
from flight_data import FlightData
from notification_manager import NotificationManager

# API Credentials
API_KEY_AMADEUS = "<your_api_key>"
API_SECRET_AMADEUS = "<your_api_secret_key>"

# Email Credentials
EMAIL_SENDER = "<your_email_address>"
EMAIL_PASSWORD = "<your_email_password>"
EMAIL_RECEIVER = "<your_email_receiver>"

# Initialize Classes
data_manager = DataManager()
flight_search = FlightSearch(API_KEY_AMADEUS, API_SECRET_AMADEUS)
notifier = NotificationManager(EMAIL_SENDER, EMAIL_PASSWORD)

# Fetch Updated Data
data_manager.get_data()

# Search for Flights
today = datetime.today() + timedelta(days=1)
flight_deals = []

for row in data_manager.sheet_data:
    row_id = row["id"]
    origin = row["iataCode"]
    destination = row["destinationCode"]
    lowest_price = float(row["lowestPrice"])
    best_flight = None

    for months_ahead in range(1, 7):
        departure_date = (today + timedelta(days=30 * months_ahead)).strftime("%Y-%m-%d")
        return_date = (today + timedelta(days=(30 * months_ahead) + 7)).strftime("%Y-%m-%d")

        flight = flight_search.search_cheapest_round_trip(origin, destination, departure_date, return_date)

        if flight:
            price = float(flight["price"]["total"])
            if price < lowest_price:
                best_flight = FlightData(origin, destination, price, departure_date, return_date)
                lowest_price = price

    if best_flight:
        flight_deals.append(str(best_flight))
        data_manager.update_price(
            row_id=row["id"],
            new_price=best_flight.price,
            departure_date=best_flight.departure_date,
            return_date=best_flight.return_date,
            destination_city=row["destinationCity"],
            destination_code=row["destinationCode"]
        )

if flight_deals:
    email_subject = "🔥 Flight Deal Alert!"
    email_body = "\n\n".join(flight_deals) + "\n\nBook now before prices rise!"
    notifier.send_email(EMAIL_RECEIVER, email_subject, email_body)
    print(f"✅ Email sent with {len(flight_deals)} flight deals.")
