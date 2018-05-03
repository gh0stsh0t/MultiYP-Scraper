import scrapy
from scrapy import Request
from bs4 import BeautifulSoup
import logging

class BDSpider(scrapy.Spider):
    name = "ypUK"

    def __init__(self, category=None, *args, **kwargs):
        super(BDSpider,self).__init__(*args, **kwargs)
        self.start_urls = ['' % category]

    def parse(self, response):
        businesses = response.css('div.listing-data')
        for business in businesses:
            yield self.getinfo(business)

        next_page = response.css('a.navigation::attr(href)').extract()
        if next_page is not None:
            if len(next_page) is 1:
                next_page = response.urljoin(next_page[0])
            elif len(next_page) is 2:
                next_page = response.urljoin(next_page[0])
            else:
                logging.info('No more pages')
        else:
            logging.info('No extra pages found')

    def getinfo(self, business):
        x = business.css('').extract_first(default="").strip()
        try:
            x = x.split(":")[1]
        except Exception as ex:
            x = x

        return {



            }


