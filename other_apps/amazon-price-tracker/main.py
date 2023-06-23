import requests
from bs4 import BeautifulSoup
import smtplib
import os

SENDER_EMAIL = os.environ.get("SENDER_EMAIL")
SENDER_EMAIL_PW = os.environ.get("SENDER_EMAIL_PW")
RECEIVE_EMAIL = os.environ.get("RECEIVE_EMAIL")
TARGET_URL = "https://www.amazon.com/Jocko-Energy-Drink-Afterburner-Orange/dp/B08LNZT23N/ref=sr_1_1_sspa?keywords" \
             "=jocko+go&qid=1685730388&sr=8-1-spons&psc=1&smid=AFZ9C51XDJJO7&spLa" \
             "=ZW5jcnlwdGVkUXVhbGlmaWVyPUFaVEdXMDhJRjlENFcmZW5jcnlwdGVkSWQ9QTA3NjI3NDAyRzVKODJMTFlXVFBIJmVuY3J5cHRlZEFkSWQ9QTA3NDI2NTExT1FDVElMSUNEMVIyJndpZGdldE5hbWU9c3BfYXRmJmFjdGlvbj1jbGlja1JlZGlyZWN0JmRvTm90TG9nQ2xpY2s9dHJ1ZQ== "
TARGET_PRICE = 35.00

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 "
                  "Safari/537.36 ",
    "Accept-Language": "en-US,en;q=0.9"
}
response = requests.get(url=TARGET_URL, headers=headers)


def get_amazon_product_info():
    amazon_page = response.text
    soup = BeautifulSoup(amazon_page, "html.parser")
    price_raw = soup.find(id="sns-base-price")
    price = float(price_raw.get_text(strip=True).split("(")[0].split("$")[1])
    name_raw = soup.find(id="productTitle")
    name = name_raw.get_text(strip=True)
    product_dict = {"name": name,
                    "price": price}
    return product_dict


def send_price_alert_email(current_price, trigger_price, target_product):
    with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
        connection.starttls()
        connection.login(user=SENDER_EMAIL, password=SENDER_EMAIL_PW)
        if current_price <= trigger_price:
            connection.sendmail(
                from_addr=SENDER_EMAIL,
                to_addrs=RECEIVE_EMAIL,
                msg=f"Subject: Amazon Low Price Alert\n\nCurrent Price:{current_price}\n\nProduct: {target_product}"
                    f"\n\nPurchase Link: {TARGET_URL}"
            )


product_info = get_amazon_product_info()
send_price_alert_email(current_price=product_info["price"], trigger_price=TARGET_PRICE,
                       target_product=product_info["name"])
