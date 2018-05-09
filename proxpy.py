from bs4 import BeautifulSoup
from random import randint
import urllib2
import requests
import logging


class proxyhandler:
    proxylist = []
    proxy = ' '
    calls = 0

    def __init__(self):
        self.get_list()
        self.get_new()
        self.get_proxy()

    def get_proxy(self):
        while True:
            if self.test_domain() and (self.calls + randint(0, 3)) < 15:
                self.calls += 1
                return self.proxy
            else:
                self.get_new()

    def get_new(self):
        while True:
            if self.proxylist:
                self.proxy = self.proxylist.pop()
                logging.info('Retrieved New Proxy: '+self.proxy+'\n')
                if not self.proxylist:
                    self.get_list()
                self.calls = 0
                return
            else:
                self.get_list()

    def get_list(self):
        page = urllib2.Request("https://www.us-proxy.org")
        page.add_header('User-Agent', 'Mozilla/5.0 (X11; U; linux i686) Gecko/20071127 Firefox/2.0.0.11')
        opener = urllib2.build_opener()
        stream = opener.open(page).read()
        soup = BeautifulSoup(stream, "lxml")
        founds = soup.find_all('td')
        found = []
        for x in founds:
            found.append(x.text)
        scraped = []
        for x in range(0, len(found)-31, 8):
            if str(found[x+6]) == 'yes':
                scraped.append("https://"+str(found[x])+":"+str(found[x+1]))
        logging.info(scraped)
        self.proxylist = scraped

    def test_domain(self):
        protocol = 'https'
        test_url = '%s://%s' % (protocol, 'www.yell.com/')
        print("testing: "+self.proxy)
        try:
            r = requests.head(test_url, timeout=1.5, proxies={'https': self.proxy})
            logging.info(r.status_code)
            logging.info(test_url)
            return True
        except (requests.exceptions.ConnectionError, requests.exceptions.ReadTimeout) as e:
            logging.info("error\n")
            return False
