import pandas as pd
import requests
from bs4 import BeautifulSoup as bs

from lib import scraping as s

class Product(object):
    def __init__(self, amazon_id):
        self.amazon_id = amazon_id
        self.response = self.get_response()
        self.soup = self.get_soup()


    @property
    def product_url(self):
        product_url = 'https://www.amazon.com/dp/'
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

    def get_soup(self):
        soup = bs(self.response.content, features='lxml')
        return soup

    def get_info(self):
        name = self.soup.find('span', attrs={'id':'productTitle'}).text.strip()
        seller = self.soup.find('div', attrs={'data-feature-name':'bylineInfo'}).find('a').text
        price = self.soup.find('span', attrs={'id':'priceblock_ourprice'}).text
        #options = list(li.attrs['data-defaultasin'] for li in self.soup.select('li[id*="color"]'))
        #details
        raw_details = self.soup.find('h2',text=r'Product details').parent
        asin = raw_details.find(text='ASIN').parent.parent.parent.text.split(': ')[-1]
        rating = raw_details.find('span',attrs={'class':'a-icon-alt'}).text.split(' out')[0]
        review_count = raw_details.find('span',attrs={'class','a-size-small'}).find('a',attrs={'class','a-link-normal'}).text.strip().split(' customer')[0]
        return {
            'name' : name,
            'seller' : seller,
            'price' : price,
            'asin' : asin,
            'rating' : rating,
            'review_count' : review_count
        }
