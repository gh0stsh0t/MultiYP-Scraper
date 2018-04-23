import scrapy
from scrapy import Request
from bs4 import BeautifulSoup
import logging
import csv

class BDSpider(scrapy.Spider):
    name = "ypUS"

    def __init__(self, category=None, *args, **kwargs):
        super(BDSpider, self).__init__(*args, **kwargs)
        self.start_urls = ["https://www.yellowpages.com/search?search_terms=%s&geo_location_terms=AL" % category]
        self.category=category 
        with open('UScities.csv') as csvfile: # Read in the csv file
            readCSV = csv.reader(csvfile, delimiter=',')
            self.zips = []
            for row in readCSV:
                zip = row[1]
            self.zips.append(zip) # Isolate the zipcodes portion of csv

    def parse(self, response):
        businesses = response.css('div.organic')
        businesses = businesses.css('div.info')
        
        for business in businesses:
            business_url = business.css('a.business-name::attr(href)').extract_first()
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
                next_page="https://www.yellowpages.com/search?search_terms={0}&geo_location_terms={1}".format(self.category, self.zips.pop(0))
                yield scrapy.Request(next_page, callback=self.parse)
            else:    
                logging.info('no more things to scrape')

    def parse_page(self, response):
        yield self.getinfo(response.xpath("//header[@id='main-header']"))

    def getinfo(self, business):
        x=business.css('a.email-business::attr(href)').extract_first(default="")
        try:
            x=x.split(':')[1]
        except Exception as ex:
            x=x

        return {
            'title': business.css('h1::text').extract_first().strip(),
            'email': x,
            'phone': business.css('p.phone::text').extract_first(default="").strip(),
            'website': business.css('a.website-link::attr(href)').extract_first(default="")
        }
