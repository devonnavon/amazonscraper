import pandas as pd
import requests
from bs4 import BeautifulSoup as bs

from lib import scraping as s

class Reviews(object):
    def __init__(self, amazon_id, count):
        self.amazon_id = amazon_id
        self.response = self.get_response()
        self.soup = self.get_soup()

    @property
    def product_url(self):
        product_url = f'https://www.amazon.com/product-reviews/B07QG5WJB1/?sortBy=recent&pageNumber={}'
        url = product_url + self.amazon_id
        return url

    def get_response(self):
        headers = {
            "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0",
            "Accept-Encoding":"gzip, deflate", "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "DNT":"1","Connection":"close", "Upgrade-Insecure-Requests":"1"
            }
        r = requests.get(self.product_url, headers=headers)
        return r
