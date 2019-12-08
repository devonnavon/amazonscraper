import pandas as pd
import requests
import sys
from bs4 import BeautifulSoup as bs


class SearchPage(object):
    def __init__(self, query, page_number=1):
        self.query = query
        self.page_number = page_number
        self.response = self.get_response()
        self.soup = self.get_soup()
        self.results = self.get_result_list()

    @property
    def search_url(self):
        search_url = 'https://www.amazon.com/s?k='
        search_text = self.query.replace(' ','+')
        url = search_url + search_text + '&page='+str(self.page_number)
        return url

    def get_response(self):
        headers = {
            "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0",
            "Accept-Encoding":"gzip, deflate", "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "DNT":"1","Connection":"close", "Upgrade-Insecure-Requests":"1"
            }
        r = requests.get(self.search_url, headers=headers)
        return r

    def get_soup(self):
        soup = bs(self.response.content, features='lxml')
        return soup

    def get_result_list(self):
        """
        gets portion of page that is just results
        """
        return self.soup.find('div', attrs={'class':'s-result-list s-search-results sg-row'})

    #non init or property functions
    def get_max_pages(self):
        """
        gets max pages displayed on page (should only be used on first page)
        """
        page_counter = self.soup.find('div', attrs={'class':'a-section a-spacing-none a-padding-base'})
        num_pages = page_counter.findAll('li', attrs={'class':'a-disabled'})[-1].text
        return int(num_pages)

    def get_product_divs(self):
        """
        gets list of product within result list
        """
        product_divs = self.results.select('div[data-asin]')
        #filter out divs that don't have amazon_id
        product_divs = list(filter(lambda x: len(x.attrs['data-asin']) > 0, product_divs))
        return product_divs

    #@staticmethod
    def get_product_info(self,div):
        """
        gets info for individual product divs
        """
        #self dummy
        amazon_id = div.attrs['data-asin']

        name = div.find('span', attrs={'class':'a-size-base-plus a-color-base a-text-normal'})
        if name is not None:
            name = name.text
        else:
            pass

        price = div.find('span', attrs={'class':'a-offscreen'})
        if price is not None:
            price = price.text
        else:
            pass

        sponsored = div.find('span', attrs={'class':'a-size-base a-color-secondary'})
        if sponsored is not None:
            is_sponsored = True
        else:
            is_sponsored = False
            
        return {
            'amazon_id' : amazon_id,
            'name' : name,
            'price' : price,
            'is_sponsored': is_sponsored
        }

    def get_products(self):
        """
        uses get_product_divs() and get_product_info()
        """
        products = []
        for div in self.get_product_divs():
            products.append(self.get_product_info(div))
        return products
