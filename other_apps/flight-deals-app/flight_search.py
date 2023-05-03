import os
import requests


class FlightSearch:
    """This class is responsible for talking to the Flight Search API."""

    TEQUILA_API_KEY = os.environ.get("TEQUILA_API_KEY")
    TEQUILA_LOCATION_QUERY_EP = os.environ.get("TEQUILA_LOCATION_QUERY_EP")
    TEQUILA_HEADERS = {
        'Content-Type': 'application/json',
        'apikey': TEQUILA_API_KEY,
    }

    def __init__(self):
        self.iata_search_payload = {}

    def find_iata_code(self, city_name=""):
        self.iata_search_payload = {
            "term": city_name,
            "locale": "en-US",
            "location_types": "city"
        }
        response = requests.get(url=self.TEQUILA_LOCATION_QUERY_EP, headers=self.TEQUILA_HEADERS,
                                params=self.iata_search_payload)
        response.raise_for_status()
        data = response.json()
        locations_list = data["locations"]
        for x in range(len(locations_list)):
            if locations_list[x]["name"].lower() == city_name.lower():
                target_iata_code = locations_list[x]["code"]
            else:
                target_iata_code = "Not Found"
            return target_iata_code
