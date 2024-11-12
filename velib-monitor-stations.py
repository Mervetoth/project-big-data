import json
from kafka import KafkaConsumer
from pymongo_get_database import get_database
from dateutil import parser

# Parse the expiry date
expiry_date = '2021-07-13T00:00:00.000Z'
expiry = parser.parse(expiry_date)

# Set up MongoDB connection
dbname = get_database()
collection_name = dbname["station"]

# Initialize Kafka Consumer
stations = {}
consumer = KafkaConsumer("velib-stations", bootstrap_servers='localhost:9092', group_id="velib-monitor-stations")

# Process messages from Kafka
for message in consumer:
    # Decode the message from Kafka
    station = json.loads(message.value.decode())
    station_number = station["number"]
    contract = station["contract_name"]
    available_bike_stands = station["available_bike_stands"]

    # Initialize the city station information
    if contract not in stations:
        stations[contract] = {}
    city_stations = stations[contract]

    # Check if the station is already tracked
    if station_number not in city_stations:
        city_stations[station_number] = available_bike_stands

    # Calculate the difference in available bike stands
    count_diff = available_bike_stands - city_stations[station_number]
    if count_diff != 0:
        city_stations[station_number] = available_bike_stands
        print("{}{} {} ({})".format(
            "+" if count_diff > 0 else "",
            count_diff, station["address"], contract
        ))

        # Insert the station data into MongoDB
        collection_name.insert_one({
            "station_number": station_number,
            "contract_name": contract,
            "address": station["address"],
            "available_bike_stands": available_bike_stands,
            "timestamp": station.get("timestamp", None)  # Use timestamp if available
        })
