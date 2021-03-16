import requests
from bs4 import BeautifulSoup
from os import system, name, getenv
from twilio.rest import Client
import time
from datetime import datetime


def send_text(message):
    client = Client(getenv("TWILIO_ACCOUNT_SID"),
                    getenv("TWILIO_AUTH_TOKEN"))
    message = client.messages.create(
        body=message,
        from_=getenv("TWILIO_FROM_NUMBER"),
        to=getenv("WIFES_PHONE"),
    )

def get_page_html(url):
    headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36"}
    page = requests.get(url, headers=headers)
    if page.status_code == 200:
        return page.content
    return None


def check_item_in_stock(page_html):
    soup = BeautifulSoup(page_html, 'html.parser')
    out_of_stock_divs = soup.findAll("button", {"data-lulu-track": "pdp-add-to-bag-regular-enabled"})
    print("{}".format(out_of_stock_divs))
    return len(out_of_stock_divs) != 0

def check_inventory(url):
    page_html = get_page_html(url)
    if page_html is not None:
        if check_item_in_stock(page_html):
            print("{:88} - [In stock]".format(url))
            send_text("Lululemon Align Cassis IN STOCK {url}".format(url=url))
            exit()
        else:
            print("{:88} - [Out of stock]".format(url))

if __name__ == "__main__":
    url = "https://shop.lululemon.com/p/women-pants/Align-Pant-Tall/_/prod9410067?color=26950&sz=12"
    while True:
        print("{} - Checking inventory...".format(datetime.now()))
        check_inventory(url)
        time.sleep(600)
