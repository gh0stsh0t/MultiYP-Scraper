import scrapy
from scrapy import Request
from scrapy.linkextractors import LinkExtractor
from bs4 import BeautifulSoup
import logging
import csv
import re


class EPSpider(scrapy.Spider):
    name = "epALL"
    custom_settings = {
        'AUTOTHROTTLE_ENABLED': 'False',
        'DEPTH_LIMIT': 2
        }

    def __init__(self, content=None, *args, **kwargs):
        super(EPSpider, self).__init__(args, **kwargs)
        with open(content+'.csv') as csvfile:
            readCSV = csv.DictReader(csvfile)
            self.zips = []
            self.sites = []
            self.titles = {}
            self.linkers = LinkExtractor(allow=(), deny=('yahoo.com'), unique=True)
            for row in readCSV:
                if row['website'] is not '':
                    url = re.sub(r"https?://(www\.)?", 'http://', row['website'], 1)
                    url = re.sub(r"\/$", "", url, 1)
                    self.sites.append(url)
                    self.titles[url] = row['title']

            logging.info(len(self.sites))
            #logging.info(self.titles['http://www.mikeandedsbbq.com'])
            self.start_urls = self.sites

    def fn_bits(self, n):
        while n:
            b = n & (~n+1)
            yield b
            n ^= b

    def parse(self, response):
        sitedata = response.meta.get('sitedata')
        if sitedata is None:
            url = re.sub(r"https?://(www\.)?", 'http://', response.request.url, 1)
            url = re.sub(r"\/$", "", url, 1)
            sitedata = metadata(response.request.url, self.titles[url])

        soup = BeautifulSoup(response.text, 'lxml')
        soup = soup.get_text()
        for flag in self.fn_bits(sitedata.flags):
            if flag == 1:
                sitedata.email = self.finder(soup, False)
                if sitedata.email is not None:
                    sitedata.flags -= 1
            elif flag == 2:
                sitedata.phone = self.finder(soup, True)
                if sitedata.phone is not None:
                    sitedata.flags -= 2
        if sitedata.flags == 0:
            yield {
                'title': sitedata.title,
                'email': sitedata.email,
                'phone': sitedata.phone,
                'website': sitedata.site
            }
        else:
            links = self.linkers.extract_links(response)
            links = [link for link in links if sitedata.site in link.url]
            for link in links:
                url = response.urljoin(link.url)
                yield Request(url, callback=self.parse, meta={'sitedata': sitedata})

    def finder(self, response, flag):
        #toDO: Regex for all+start url nlg
        #reason: lunch time
        if flag:
            container = re.findall(r"((?:\d{3}|\(\d{3}\))?(?:\s|-|\.)?\d{3}(?:\s|-|\.)\d{4})", response)
        else:
            container = re.findall(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,3}", response)

        if len(container) > 0:
            return container[0]
        else:
            return None


class metadata:

    def __init__(self, site, title):
        self.email = None
        self.title = title
        self.phone = None
        self.flags = 3
        self.site = site
