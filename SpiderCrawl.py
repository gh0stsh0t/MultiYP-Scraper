from twisted.internet import reactor
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from scrapy import spiderloader
def main():
    filename = raw_input("\nEnter output filename: ")
    cat = raw_input("Enter category: ")
    print("")
    settings = get_project_settings()

    settings.set('FEED_FORMAT', 'csv', priority='cmdline')
    settings.set('FEED_URI', filename+'.csv', priority='cmdline')

    process = CrawlerProcess(settings)

    spider_loader = spiderloader.SpiderLoader.from_settings(settings)
    spiders = spider_loader.list()
    print("")
    x = 1
    for spider in spiders:
        print(str(x)+". "+spider)
        x += 1
    choice = int(raw_input("Enter choice: "))
    process.crawl(spiders[choice-1], category=cat)
    process.start()

    print("\nRemoving Duplicate Entries")
    with open(filename+'.csv', 'r') as in_file, open(filename+'cleaned.csv', 'w') as out_file:
        seen = set()  # set for fast O(1) amortized lookup
        for line in in_file:
            if line in seen:
                continue  # skip duplicate

            seen.add(line)
            out_file.write(line)

    print("Process Finished")
