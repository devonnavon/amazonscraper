import multiprocessing
import threading
import time
import requests
from bs4 import BeautifulSoup as bs


class Page(object):
    def __init__(self, url):
        self.url = url

    def set_args(self, arg):
        url.format(arg)

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

    def get_info():
        pass


class Runner(object):
    def __init__(self, runs):
        self.runs = runs
        self.q = multiprocessing.Queue()
        self.t = {} #empty dict of threads or processes
        self.page = page
        self.results = [] #empty till run

    def put_page(self, arg):
        self.page.set_args(args)
        self.q.put(self.page.get_info())

    def run(self, run_info=False):
        results = []
        startTime = time.time()
        qcount = 0

        for arg in self.runs:
            self.p[arg] = threading.Thread(target=self.put_page, args=arg)
            p[page_num].start()

        for thread in self.t:
            thread.join()

        while not q.empty():
            queue_top = q.get()
            self.qcount += 1
            self.results+=queue_top

        self.run_time = time.time()-startTime

    def get_results(self):
        return self.results
