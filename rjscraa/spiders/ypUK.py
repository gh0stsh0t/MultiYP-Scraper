import scrapy 
from scrapy import Request
from bs4 import BeautifulSoup
import logging

class BDSpider(scrapy.Spider):
    name = "ypUK"

    def __init__(self, category=None, *args, **kwargs):
        super(BDSpider,self)
        
