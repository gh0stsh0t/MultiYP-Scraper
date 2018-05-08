from bs4 import BeautifulSoup
from random import randint
import urllib2
import re
import requests

class proxyhandler:
    proxylist = []
    proxy = ' '
    calls = 0

    def __init__(self):
        self.get_list()
        self.get_new()

    def get_proxy(self):
        while True:
            if self.test_domain() and (self.calls + randint(0,3)) < 15:
                self.calls += 1
                return self.proxy
            else:
                self.get_new()

    def get_new(self):
        while True:
            if self.proxylist:
                while not self.test_domain():
                    self.proxy = self.proxylist.pop()
                    print(self.proxy)
                    if not self.proxylist:
                        self.get_list()
                print('success?')
                calls = 0
                return
            else:
                self.get_list()

    def get_list(self):
        page = urllib2.Request("https://www.us-proxy.org")
        page.add_header('User-Agent','Mozilla/5.0 (X11; U; linux i686) Gecko/20071127 Firefox/2.0.0.11')
        opener = urllib2.build_opener()
        stream = opener.open(page).read()
        soup = BeautifulSoup(stream, "lxml")
        founds = soup.find_all('td')
        found = []
        for x in founds:
            found.append(x.text)
        scraped = []
        for x in range(0,len(found)-31,8):
            if str(found[x+6]) == 'yes':
                scraped.append("https://"+str(found[x])+":"+str(found[x+1]))
        print(scraped)
        self.proxylist = scraped

    def test_domain(self):
        protocol = 'https' 
        test_url = '%s://%s' % (protocol, 'www.yellowpages.com')
        print(self.proxy)
        try:
            r = requests.head(test_url, timeout=1, proxies={'https':self.proxy})
            print(r.status_code)
            print(test_url)
            return True
        except (requests.exceptions.ConnectionError, requests.exceptions.ReadTimeout) as e:
            print("error")
            return False
