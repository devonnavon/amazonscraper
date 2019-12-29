import multiprocessing
import threading
import time
import requests
from bs4 import BeautifulSoup as bs


class Page(object):
    def __init__(self, base_url):
        self.base_url = base_url

    def set_args(self, page_num, *args):
        self.url = self.base_url.format(page_num=page_num, *args)

    def get_response(self):
        headers = {
            "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0",
            "Accept-Encoding":"gzip, deflate", "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "DNT":"1","Connection":"close", "Upgrade-Insecure-Requests":"1"
            }
        self.response = requests.get(self.url, headers=headers)

    def get_soup(self):
        self.get_response()
        self.soup = bs(self.response.content, features='lxml')

    def get_info():#will want to rewrite this every time
        self.get_soup()
        return None

class Search(Page):
    def __init__(self):
        self.base_url = 'https://www.amazon.com/s?k={}&page={page_num}'

    def get_info(self):
        self.get_soup() #runs self.soup
        results = self.soup.find('div', attrs={'class':'s-result-list s-search-results sg-row'})
        product_divs = results.select('div[data-asin]')
        product_divs = list(filter(lambda x: len(x.attrs['data-asin']) > 0, product_divs))
        products = []
        for div in product_divs:
            amazon_id = div.attrs['data-asin']

            #must be a more elegant way to do this
            name = div.find('span', attrs={'class':'a-size-base-plus a-color-base a-text-normal'})
            if name is not None:
                name = name.text
            else:
                name = div.find('span', attrs={'class':'a-size-medium a-color-base a-text-normal'})
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

            products.append({
                'amazon_id' : amazon_id,
                'name' : name,
                'price' : price,
                'is_sponsored': is_sponsored
            })
        return products

class Runner(object):
    def __init__(self, page):
        self.q = multiprocessing.Queue()
        self.t = {} #empty dict of threads or processes
        self.page = page #page object

    def put_page(self, page_num, *args):
        self.page.set_args(page_num, *args)
        self.q.put(self.page.get_info())

    def run(self, pages, *args):
        '''
        pages int for number of pages to get
        args = page parameters
        '''
        self.qcount = 0 #empty till run
        self.results = [] #empty till run
        self.start_time = time.time()
        qcount = 0

        for page_num in range(1, pages+1):
            #temp = (page_num,)+args
            self.t[page_num] = threading.Thread(target=self.put_page, args=(page_num,)+args)
            self.t[page_num].start()

        for thread in self.t:
            self.t[thread].join()

        while not self.q.empty():
            queue_top = self.q.get()
            self.qcount += 1
            self.results+=queue_top

        self.run_time = time.time()
        self.time_elapsed = self.run_time-self.start_time
        self.run_info = {
                        'queue_count': self.qcount,
                        'time_elapsed': self.time_elapsed,
                        'run_time': self.run_time
                        }
        return self.run_info

    def get_results(self):
        return self.results
