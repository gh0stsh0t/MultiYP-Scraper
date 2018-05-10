import scrapy
from scrapy import Request
from bs4 import BeautifulSoup
import logging
import csv
import sys

class YPSpider(scrapy.Spider):
    name = "ypUK"
    custom_settings = {
            'FEED_EXPORT_FIELDS': ['title', 'phone', 'website','country'],
            'DOWNLOADER_MIDDLEWARES': {'rjscraa.middlewares.ProxpyRotator': 500,
                'rjscraa.middlewares.RandomUserAgentMiddleware': 400,
}
            }
    handle_httpstatus_list = [404, 500]

    def __init__(self, category=None, state=None, *args, **kwargs):
        super(YPSpider, self).__init__(*args, **kwargs)
        self.category = category
        with open('UKpostcodes.csv') as csvfile:  # Read in the csv file
            readCSV = csv.reader(csvfile, delimiter=',')
            self.zips = []
            states = []
            logging.info(state)
            for row in readCSV:
                states.append(row[0])

            if state is None:
                self.zips.extend(states)  # Isolate the zipcodes portion of csv
            else:
                state = state.split(',')
                state = [int(i) for i in state]
                state = list(set(state))
                for x in state:
                    try:
                        self.zips.append(states[x-1])
                    except Exception:
                        sys.exc_clear()

            logging.info("Postcodes to go through: "+str(self.zips))
            # toDO: o(n+2k) make into o(n)

        next_page = "https://www.yell.com/ucs/UcsSearchAction.do?keywords={0}&location={1}".format(category, self.zips.pop(0))
        self.start_urls = [next_page]


    def parse(self, response):
        if response.status == 404:
            logging.info("Encountered 404 popping next postcode")
            next_page = "https://www.yell.com/ucs/UcsSearchAction.do?keywords={0}&location={1}".format(self.category, self.zips.pop(0))
            yield scrapy.Request(next_page, callback=self.parse)
        else:
            businesses = response.css('div.businessCapsule--mainContent')
            for business in businesses:
                yield self.getinfo(business)

            next_page = response.css('a.pagination--next::attr(href)').extract_first()
            if next_page is not None:
                next_page = response.urljoin(next_page)
                yield scrapy.Request(next_page, callback=self.parse)
            elif len(self.zips) > 0:
                next_page = "https://www.yell.com/ucs/UcsSearchAction.do?keywords={0}&location={1}".format(self.category, self.zips.pop(0))
                yield scrapy.Request(next_page, callback=self.parse)
            else:
                logging.info('no more things to scrape')


    def getinfo(self, business):
        x = business.css('a.businessCapsule--ctaItem::attr(href)').extract()
        if x:
            x = x[len(x)-1]
        else:
            x = ''

        return {
            'title': business.css('h2.text-h2::text').extract_first(default="").strip(),
            'phone': business.css('span.business--telephoneNumber::text').extract_first(default="").strip(),
            'website': x,
            'country': 'United Kingdom'
        }


