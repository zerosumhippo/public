import os
import smtplib


class NotificationManager:
    """This class is responsible for sending notifications with the deal flight details."""

    FROM_EMAIL = os.environ.get("FROM_EMAIL")
    TO_EMAIL = os.environ.get("TO_EMAIL")
    EMAIL_PASSWORD = os.environ.get("EMAIL_PASSWORD")

    def __init__(self):
        self.flight_filename = "flight_info.csv"

    def send_notification(self, message_data=[]):
        if len(message_data) > 0:
            file_truncate_task = open(self.flight_filename, "w+")
            file_truncate_task.close()
            for x in range(len(message_data)):
                flight_datetime = message_data[x]["outbound_date"]
                flight_date = flight_datetime.split("T", 1)[0]
                flight_time = flight_datetime.split("T", 2)[1]
                with open(self.flight_filename, mode="a") as file:
                    file.write(f"\nFlight Option {x + 1}:\n"
                               f"Only ${message_data[x]['price']} to fly from "
                               f"{message_data[x]['departure_city_name']} to "
                               f"{message_data[x]['arrival_city_name']} on {flight_date} at {flight_time}."
                               f"\nBooking Link: {message_data[x]['link']}\n")
            with open(self.flight_filename) as file:
                contents = file.read()
                with smtplib.SMTP("smtp.gmail.com") as connection:
                    connection.starttls()
                    connection.login(user=self.FROM_EMAIL, password=self.EMAIL_PASSWORD)
                    connection.sendmail(
                        from_addr=self.FROM_EMAIL,
                        to_addrs=self.TO_EMAIL,
                        msg=f"Subject:Low Price Flight Alert\n\n{contents}"
                    )
