import requests
from bs4 import BeautifulSoup
from os import system, name, getenv
from twilio.rest import Client
import time


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
    print(page.status_code)
    return page.content


def check_item_in_stock(page_html):
    soup = BeautifulSoup(page_html, 'html.parser')
    out_of_stock_divs = soup.findAll("button", {"data-lulu-track": "pdp-add-to-bag-regular-enabled"})  # <--- change "text" to div
    print(out_of_stock_divs)
    return len(out_of_stock_divs) != 0

def check_inventory(url):
    page_html = get_page_html(url)
    if check_item_in_stock(page_html):
        print("In stock")
        send_text("Lululemon Align Cassis IN STOCK {url}".format(url=url))
        exit()
    else:
        print("Out of stock")

if __name__ == "__main__":
    url = "https://shop.lululemon.com/p/women-pants/Align-Pant-Tall/_/prod9410067?color=26950&sz=12"
    while True:
        check_inventory(url)
        time.sleep(1800)