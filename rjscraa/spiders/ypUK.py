import scrapy
from scrapy import Request
from bs4 import BeautifulSoup
import logging


class BDSpider(scrapy.Spider):
    name = "ypUK"
    custom_settings = {
            'FEED_EXPORT_FIELDS': ['title', 'phone', 'website','country']
            }

    def __init__(self, category=None, *args, **kwargs):
        super(BDSpider, self).__init__(*args, **kwargs)
        self.start_urls = ['' % category]

    def parse(self, response):
        businesses = response.css('div.businessCapsule--mainContent')
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
        x = business.css('a.businessCapsule--ctaItem::attr(href)').extract()
        if len(x) > 1:
            x = x[1]

        return {
            'title': business.css('a.businessCapsule--name::text').extract_first().strip(),
            'phone': business.css('span.business--telephoneNumber::text').extract_first().strip(),
            'website': x,
            'country': 'United Kingdom'
        }
