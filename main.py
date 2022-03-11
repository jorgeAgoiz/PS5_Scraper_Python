from time import sleep
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import os
import smtplib
import ssl
from email.mime.text import MIMEText

load_dotenv()
my_headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "Accept-Language": "es-ES,es;q=0.9,de;q=0.8,en;q=0.7",
    "Accept-Encoding": "gzip, deflate, br"
}

EMAIL_PASS = os.getenv('EMAIL_PASS')

# To Send Emails
sender = os.getenv('EMAIL_ACCOUNT')
receiver = os.getenv('EMAIL_RECIEVER')

# Pages to buy Playstation 5

pages = [
    {
        "URL": "https://www.game.es/consola-playstation-5-playstation-5-183224",
        "shop": "game"
    },
    {
        "URL": "https://www.amazon.es/Sony-PlayStation-Consola-5/dp/B08H93ZRK9/ref=sr_1_3?__mk_es_ES=%C3%85M%C3%85%C5%BD%C3%95%C3%91&crid=343P2VYPCS9SK&keywords=ps5+consola&qid=1646980681&s=videogames&sprefix=ps5+consola%2Cvideogames%2C74&sr=1-3",
        "shop": "amazon"
    },
    {
        "URL": "https://www.elcorteingles.es/videojuegos/A37046604-consola-playstation-5/",
        "shop": "eci"
    }
]

# Functions to make scraping


def stock_amazon(soup):
    element_stock = soup.find("span", id="submit.buy-now-announce")
    if element_stock is not None and element_stock.get_text().strip() == "Comprar ya":
        return True
    else:
        return False


def stock_game(soup):
    element_stock = soup.find(
        "a", class_="buy--btn btn btn-new btn-circle icon-wrap buy-button")
    if element_stock is not None:
        return True
    else:
        return False


def stock_eci(soup):
    element_stock = soup.find("input", id="product_not_avalible")
    if element_stock is not None:
        return True
    else:
        return False


for page in pages:  # Iterate the shop pages
    sleep(1)

    try:
        website = requests.get(page["URL"], headers=my_headers)
        soup = BeautifulSoup(website.content, "html5lib")

        if page["shop"] == "eci":
            result = stock_eci(soup)
        if page["shop"] == "game":
            result = stock_game(soup)
        if page["shop"] == "amazon":
            result = stock_amazon(soup)

        if result:
            body_email = f'You have stock in {page["shop"]}, click in the url: {page["URL"]}'
            msg = MIMEText(body_email, 'html')
            msg['Subject'] = 'STOCK NOTICE'
            msg['From'] = sender
            msg['To'] = receiver
            s = smtplib.SMTP_SSL(host='smtp.gmail.com', port=465)
            s.login(user=sender, password=EMAIL_PASS)
            s.sendmail(sender, receiver, msg.as_string())
            s.quit()
    except:
        print("Something Went Wrong")
