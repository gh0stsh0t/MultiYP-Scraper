import os
import sys
sys.path.append('pkgs')
from twisted.internet import reactor
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from scrapy import spiderloader


class KickStarter:

    def __init__(self):
        self.settings = get_project_settings()

    def start_crawl(self, choice, category, filename, state=None):
        
        self.settings.set('FEED_FORMAT', 'csv', priority='cmdline')
        self.settings.set('FEED_URI', filename+'.csv', priority='cmdline')

        process = CrawlerProcess(self.settings)
        process.crawl(choice, category=category, state=state)
        process.start()

        print("Process Finished")


if __name__== '__main__':
    x = KickStarter()
    if len(sys.argv) < 5:
        sys.argv.append(None)
    x.start_crawl(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
