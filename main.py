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
        return page.content, page.status_code
    return None, page.status_code


def check_item_in_stock(page_html):
    soup = BeautifulSoup(page_html, 'html.parser')
    out_of_stock_divs = soup.findAll("button", {"data-lulu-track": "pdp-add-to-bag-regular-enabled"})
    print("{}".format(out_of_stock_divs))
    return len(out_of_stock_divs) != 0


def check_inventory(url):
    status_code = 0
    page_html = None
    counter = 0
    max_retries = 24
    sleep = 300
    while status_code != 200 and page_html is None and counter < max_retries:
        counter += 1
        try:
            print("{} - Checking products for availability attempt #{}...".format(str(datetime.now()), counter))
            page_html, status_code = get_page_html(url)
        except Exception as e:
            time.sleep(sleep)

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
        check_inventory(url)
        time.sleep(600)
