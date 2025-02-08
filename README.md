Features
Fetches real-time flight prices using the Amadeus API.
Automatically compares new prices with historical prices stored in Google Sheets.
Filters flight data based on travel duration and stopovers to find optimal routes.
Sends email notifications when a cheaper flight deal is detected.
OAuth2 authentication for secure API access.
Designed for scalability, easily extensible for other APIs or additional filtering criteria.
Requirements
Python 3.7+
API Key and Secret for Amadeus API (sign up at Amadeus for Developers)
Google Sheets API key (via Sheety API - Sheety)
SMTP email credentials (for email notifications)
Setup Instructions
1. Install Dependencies
Clone the repository and install the required packages:

bash

git clone https://github.com/yourusername/flight-deal-finder.git
cd flight-deal-finder
pip install -r requirements.txt

2. Configure API Keys
Replace API_KEY_AMADEUS and API_SECRET_AMADEUS with your Amadeus API credentials.
Set up Google Sheets API via Sheety and replace the endpoint URL in the code.
Enter your SMTP email credentials (email sender, password) in the script.
3. Running the Application
To start the flight search and send email alerts:

bash

python flight_search.py
The script will fetch flight data, compare prices, and notify you of any deals via email.

File Descriptions
flight_search.py: Main script responsible for flight search using Amadeus API, price comparison, and sending email alerts.
data_manager.py: Handles interactions with Google Sheets to fetch and update flight data.
notification_manager.py: Sends email notifications with flight deal details.
flight_data.py: Defines the data structure for storing flight information.

How It Works
Data Fetching: The script fetches flight data from the Amadeus API using the search_cheapest_round_trip method.
Price Comparison: Compares current prices to stored prices from Google Sheets using the Sheety API.
Price Update: If a better deal is found, it updates the Google Sheet with the new price and flight details.
Email Notification: Sends an automated email notification to the user using SMTP whenever a cheaper flight is found.

Contributing
If you'd like to contribute to this project, feel free to fork the repository, make your changes, and submit a pull request.

License
This project is licensed under the MIT License - see the LICENSE file for details.
