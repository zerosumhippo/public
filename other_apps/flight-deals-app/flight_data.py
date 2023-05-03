import os
import requests
import datetime


class FlightData:
    """This class is responsible for structuring the flight data."""

    TEQUILA_API_KEY = os.environ.get("TEQUILA_API_KEY")
    TEQUILA_SEARCH_EP = os.environ.get("TEQUILA_SEARCH_EP")
    TEQUILA_HEADERS = {
        'Content-Type': 'application/json',
        'apikey': TEQUILA_API_KEY,
    }
    TOMORROW = (datetime.date.today() + datetime.timedelta(days=1)).strftime("%d/%m/%Y")
    MAX_DEPART_DATE = (datetime.date.today() + datetime.timedelta(days=180)).strftime("%d/%m/%Y")

    def __init__(self):
        self.find_flight_payload = None
        self.departure_airport_code = "MCI"
        self.departure_city = "Kansas City"
        self.flights_info = []

    def find_lowest_price_flight(self, dest_iata_code="", low_price_on_record=0):
        self.find_flight_payload = {
            "fly_from": self.departure_airport_code,
            "fly_to": dest_iata_code,
            "date_from ": self.TOMORROW,
            "date_to ": self.MAX_DEPART_DATE,
            # "flight_type ": "round",
            # "nights_in_dst_from ": 6,
            # "nights_in_dst_to ": 27,
            "adults": 1,
            "curr": "USD",
            "locale": "en",
            "max_stopovers": 0,
        }
        response = requests.get(url=self.TEQUILA_SEARCH_EP, headers=self.TEQUILA_HEADERS,
                                params=self.find_flight_payload)
        response.raise_for_status()
        data = response.json()
        flights = data["data"]
        price_list = []
        for x in range(len(flights)):
            price_list.append(flights[x]["price"])
        price_list.sort()
        lowest_price = price_list[0]
        for x in range(len(flights)):
            if flights[x]["price"] == lowest_price and flights[x]["price"] <= low_price_on_record:
                ind_flight_dict = {
                    "departure_city_name": self.departure_city,
                    "departure_airport_iata_code": self.departure_airport_code,
                    "arrival_city_name": flights[x]["cityTo"],
                    "arrival_airport_iata_code": flights[x]["flyTo"],
                    "outbound_date": flights[x]["local_departure"],
                    "price": flights[x]["price"],
                    "link": flights[x]["deep_link"],
                }
                self.flights_info.append(ind_flight_dict)
        return lowest_price
