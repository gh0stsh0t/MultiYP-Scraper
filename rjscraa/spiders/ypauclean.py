import scrapy
from scrapy import Request
from bs4 import BeautifulSoup
import logging


class BDSpider(scrapy.Spider):
    name = "rjscraa"

    def __init__(self, category=None, *args, **kwargs):
        super(BDSpider, self).__init__(*args, **kwargs)
        self.start_urls = ['https://www.yellowpages.com.au/search/listings?clue=%s' % category]

    def parse(self, response):
        businesses = response.css('div.listing-data')

        for business in businesses:
            #yield self.parse_page(business)
            x = business.css('a.contact-phone::attr(href)').extract_first(default="").strip()
            try:
                x = x.split(":")[1]
            except Exception as ex:
                print("heh")

            yield {
                'title': business.css('a.listing-name::text').extract_first().strip(),
                'email': business.css('a.contact-email::attr(data-email)').extract_first(default=""),
                'phone': x,
                'website': business.css('a.contact-url::attr(href)').extract_first(default="")
            }

        next_page = response.css('a.navigation::attr(href)').extract()
        if next_page is not None:
            if len(next_page) is 1:
                next_page = response.urljoin(next_page[0])
            elif len(next_page) is 2:
                next_page = response.urljoin(next_page[1])
            logging.info(next_page)
            print(next_page)
            yield scrapy.Request(next_page, callback=self.parse)
        else:
            logging.info('no more things to scrape')
            print('no more things to scrape')
