import scrapy
from scrapy import Request
from bs4 import BeautifulSoup
import logging
import csv
import sys


class YPSpider(scrapy.Spider):
    name = "ypUS"

    def __init__(self, category=None, state=None, *args, **kwargs):
        super(YPSpider, self).__init__(*args, **kwargs)
        self.category = category
        if state:
            self.zips=state.split(',')
        else:
            with open('UScities.csv') as csvfile:  # Read in the csv file
                readCSV = csv.reader(csvfile, delimiter=',')
                self.zips = []
                for row in readCSV:
                    self.zips.append(row[1])
                
        logging.info("States to go through: "+str(self.zips))
        next_page = "https://www.yellowpages.com/search?search_terms={0}&geo_location_terms={1}".format(
            category, self.zips.pop(0))
        self.start_urls = [next_page]

    def parse(self, response):
        businesses = response.css('div.organic').css('div.info')

        for business in businesses:
            business_url = business.css(
                'a.business-name::attr(href)').extract_first()
            business_url = response.urljoin(business_url)
            logging.info(business_url)
            yield Request(business_url, callback=self.parse_page)

        next_page = response.css('a.next::attr(href)').extract_first()

        if next_page is not None:
            next_page = response.urljoin(next_page)
            logging.info(next_page)
            print(next_page)
            yield scrapy.Request(next_page, callback=self.parse)
        else:
            if len(self.zips) > 0:
                next_page = "https://www.yellowpages.com/search?search_terms={0}&geo_location_terms={1}".format(
                    self.category, self.zips.pop(0))
                yield scrapy.Request(next_page, callback=self.parse)
            else:
                logging.info('no more things to scrape')

    def parse_page(self, response):
        yield self.getinfo(response.xpath("//header[@id='main-header']"))

    def getinfo(self, business):
        x = business.css(
            'a.email-business::attr(href)').extract_first(default="")
        try:
            x = x.split(':')[1]
        except Exception:
            sys.exc_clear()

        return {
            'title': business.css('h1::text').extract_first().strip(),
            'email': x,
            'phone': business.css('p.phone::text').extract_first(default="").strip(),
            'website': business.css('a.website-link::attr(href)').extract_first(default=""),
            'country': 'USA'
        }
