from time import sleep
import requests
from bs4 import BeautifulSoup
import sys

# Pages to buy Playstation 5
pages = [
    "https://www.amazon.es/Sony-PlayStation-Consola-5/dp/B08H93ZRK9/ref=sr_1_3?__mk_es_ES=%C3%85M%C3%85%C5%BD%C3%95%C3%91&crid=343P2VYPCS9SK&keywords=ps5+consola&qid=1646980681&s=videogames&sprefix=ps5+consola%2Cvideogames%2C74&sr=1-3",
    "https://www.game.es/consola-playstation-5-playstation-5-183224",
    "https://www.elcorteingles.es/videojuegos/A37046604-consola-playstation-5/"
]

for page in pages:
    website = requests.get(page)
    soup = BeautifulSoup(website.content, "html5lib")
    print(soup)
    sleep(2)
