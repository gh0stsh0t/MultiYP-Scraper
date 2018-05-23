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
        'DEPTH_LIMIT': 2,
        'LOG_LEVEL': 'INFO',
        'CONCURRENT_REQUESTS':  250,
        'REACTOR_THREADPOOL_MAXSIZE': 40,
        'RETRY_ENABLED': 'False',
        'FEED_EXPORT_FIELDS': ['title', 'email', 'phone', 'website', 'country']
    }

    def __init__(self, content=None, *args, **kwargs):
        super(EPSpider, self).__init__(*args, **kwargs)
        self.zips = []
        self.sites = []
        self.descriptors = {}
        self.linkers = LinkExtractor(allow=(), deny=('yahoo.com'), unique=True)
        with open(content+'.csv') as csvfile:
            readCSV = csv.DictReader(csvfile)
            for row in readCSV:
                if row['website'] is not '':
                    row['website'] = re.sub(r"\?utm_source=yell&utm_medium=referral&utm_campaign=yell", '', row['website'])
                    self.sites.append(row['website'])
                    url = re.sub(r"https?://(www\.)?",
                                 'http://', row['website'], 1)
                    url = url.split('.')
                    if row['phone'] is '':
                        row['phone'] = None
                    self.descriptors[url[0]] = {'title': row['title'], 'country': row['country'], 'phone': row['phone']}

            logging.info("Number of Sites to crawl: "+str(len(self.sites)))
            self.start_urls = self.sites

    def fn_bits(self, n):
        while n and n >= 0:
            b = n & (~n+1)
            yield b
            n ^= b

    def parse(self, response):
        sitedata = response.meta.get('sitedata')
        if sitedata is None:
            url = re.sub(r"https?://(www\.)?", 'http://', response.request.url, 1)
            url = url.split('.')[0]
            try:
                descriptor = self.descriptors[url]
                sitedata = metaData(response.request.url, descriptor['title'], descriptor['country'], descriptor['phone'])
            except KeyError:
                raise StopIteration
        try:
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
                item = rjItem({
                    'title': sitedata.title,
                    'email': sitedata.email,
                    'phone': sitedata.phone,
                    'website': sitedata.site,
                    'country': sitedata.country
                })
                sitedata.flags -= 1
                yield item
            elif sitedata.flags > 0:
                links = self.linkers.extract_links(response)
                links = [link for link in links if sitedata.site in link.url]
                for link in links:
                    #logging.info(str(sitedata.flags)+' '+sitedata.title)
                    if sitedata.flags == 0:
                        break
                    url = response.urljoin(link.url)
                    yield Request(url, callback=self.parse, meta={'sitedata': sitedata})

        except AttributeError:
            logging.info("Skipping this page")

    def finder(self, response, flag):
        if flag:
            container = re.findall(r"^(((\+44\s?\d{4}|\(?0\d{4}\)?)\s?\d{3}\s?\d{3})|((\+44\s?\d{3}|\(?0\d{3}\)?)\s?\d{3}\s?\d{4})|((\+44\s?\d{2}|\(?0\d{2}\)?)\s?\d{4}\s?\d{4}))(\s?\#(\d{4}|\d{3}))?$", response)
        else:
            container = re.findall(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,3}", response)

        if len(container) > 0:
            return container[0]
        else:
            return None


class metaData:

    def __init__(self, site, title, country, phone=None):
        self.email = None
        self.title = title
        self.phone = phone
        self.flags = 1 if phone else 3
        self.site = site
        self.country = country


class rjItem(scrapy.Item):
    email = scrapy.Field()
    title = scrapy.Field()
    phone = scrapy.Field()
    country = scrapy.Field()
    website = scrapy.Field()
