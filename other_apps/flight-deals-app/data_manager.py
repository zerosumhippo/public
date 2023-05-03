import os
import requests


class DataManager:
    """This class is responsible for talking to the Google Sheet."""

    SHEETY_ADD_ROW_EP = os.environ.get("SHEETY_ADD_ROW_EP")
    SHEETY_GET_EP = os.environ.get("SHEETY_GET_EP")
    SHEETY_PUT_EP = os.environ.get("SHEETY_PUT_EP")
    SHEETY_AUTH = os.environ.get("SHEETY_AUTH")
    SHEETY_HEADERS = {
        'Content-Type': 'application/json',
        'Authorization': SHEETY_AUTH,
    }

    def __init__(self):
        self.sheety_payload = {}
        self.sheety_data = []

    def write_to_sheet(self):
        self.sheety_payload = {
            "price": {
                "city": "Example City",
                "iataCode": "EXP",
                "lowestPrice": 50,
            }
        }
        response = requests.post(url=self.SHEETY_ADD_ROW_EP, json=self.sheety_payload, headers=self.SHEETY_HEADERS)
        response.raise_for_status()

    def get_data(self):
        response = requests.get(url=self.SHEETY_GET_EP, headers=self.SHEETY_HEADERS)
        response.raise_for_status()
        data = response.json()
        self.sheety_data = data["prices"]
        return self.sheety_data

    def update_sheet(self, new_data=[]):
        for x in range(len(new_data)):
            self.sheety_payload = {
                "price": {
                    "iataCode": new_data[x]["iataCode"],
                    "lowestPrice": new_data[x]["lowestPrice"],
                }
            }
            response = requests.put(url=f"{self.SHEETY_PUT_EP}{new_data[x]['id']}", json=self.sheety_payload,
                                    headers=self.SHEETY_HEADERS)
            response.raise_for_status()
