import scrapy
from scrapy import Request
from bs4 import BeautifulSoup
import logging
import csv

class BDSpider(scrapy.Spider):
    name = "ypAU"

    def __init__(self, category=None, *args, **kwargs):
        super(BDSpider, self).__init__(*args, **kwargs)
        self.start_urls = ['https://www.yellowpages.com.au/search/listings?clue=%s' % category]
        with open('test.csv') as csvfile: # Read in the csv file
            readCSV = csv.reader(csvfile, delimiter=',')
            self.zips = []
            for row in readCSV:
                zip = row[0]

            self.zips.append(zip) # Isolate the zipcodes portion of csv
            logging.info(self.zips)

    def parse(self, response):
        businesses = response.css('div.listing-data')
        print(self.zip[5])
        for business in businesses:
            yield self.getinfo(business)

        next_page = response.css('a.navigation::attr(href)').extract()
        if next_page is not None:
            if len(next_page) is 1:
                next_page = response.urljoin(next_page[0])
            elif len(next_page) is 2:
                next_page = response.urljoin(next_page[1])
            else:
                logging.info('no more things to scrape')
            logging.info(next_page)
            print(next_page)
            yield scrapy.Request(next_page, callback=self.parse)
        else:
            logging.info('no more things to scrape')

    def getinfo(self, business):
        x = business.css('a.contact-phone::attr(href)').extract_first(default="").strip()
        try:
            x = x.split(":")[1]
        except Exception as ex:
            x = x

        return {
            'title': business.css('a.listing-name::text').extract_first().strip(),
            'email': business.css('a.contact-email::attr(data-email)').extract_first(default=""),
            'phone': x,
            'website': business.css('a.contact-url::attr(href)').extract_first(default="")
        }
