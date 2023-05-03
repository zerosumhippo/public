from data_manager import DataManager
from flight_search import FlightSearch
from flight_data import FlightData
from notification_manager import NotificationManager

data_manager = DataManager()
flight_search = FlightSearch()
flight_data = FlightData()
notification_manager = NotificationManager()

sheet_data = data_manager.get_data()
# sheet_data = [{'city': 'Austin', 'iataCode': 'AUS', 'lowestPrice': 200, 'id': 2}, {'city': 'Los Angeles', 'iataCode': 'LAX', 'lowestPrice': 100, 'id': 3}, {'city': 'Denver', 'iataCode': 'DEN', 'lowestPrice': 5, 'id': 4}, {'city': 'Miami', 'iataCode': 'MIA', 'lowestPrice': 5, 'id': 5}, {'city': 'Chicago', 'iataCode': 'CHI', 'lowestPrice': 5, 'id': 6}]


def update_iata_code():
    for x in range(len(sheet_data)):
        if sheet_data[x]["iataCode"] == '':
            city_name = sheet_data[x]["city"]
            iata_code_response = flight_search.find_iata_code(city_name=city_name)
            sheet_data[x]["iataCode"] = iata_code_response
            print(sheet_data)
            data_manager.update_sheet(new_data=sheet_data)


def update_flight_prices():
    for x in range(len(sheet_data)):
        lowest_price_found = flight_data.find_lowest_price_flight(dest_iata_code=sheet_data[x]["iataCode"],
                                                                  low_price_on_record=sheet_data[x]["lowestPrice"])
        if lowest_price_found <= sheet_data[x]["lowestPrice"]:
            sheet_data[x]["lowestPrice"] = lowest_price_found
            data_manager.update_sheet(new_data=sheet_data)
    notification_manager.send_notification(message_data=flight_data.flights_info)


update_iata_code()
update_flight_prices()
