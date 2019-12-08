import multiprocessing
import threading
import time

from search import page

class Search(object):
    def __init__(self, query, page_count=None):
        self.query = query
        self.page_count = page_count

    def run(self):
        search_results = []
        startTime = time.time()
        qcount = 0

        #check for pagecount and pull if none
        if self.page_count is None:
            start = 2 #already loading first page
            page1 = page.SearchPage(self.query) #load first page
            self.page_count = page1.get_max_pages() #max pages
            search_results+=page1.get_products()
        else:
            start = 1 #else start at 1

        def put_page(num, q):
            q.put(page.SearchPage(self.query, num).get_products())

        #initialize queue and empy process dict
        #m = multiprocessing.Manager()
        q = multiprocessing.Queue()
        p = {}

        #start every thread
        for page_num in range(start, self.page_count+1):
            p[page_num] = threading.Thread(target=put_page, args=(page_num,q))
            p[page_num].start()

        #join after threads have all started
        #(running join before will prevent new threads from starting)
        for page_num in range(start, self.page_count+1):
            p[page_num].join()

        while q.empty() is not True:
            qcount += 1
            queue_top = q.get()
            search_results+=queue_top

        self.results = search_results
        self.run_time = time.time()-startTime
        self.qcount = qcount
