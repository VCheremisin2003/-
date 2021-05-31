from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

from leroymerlinparser.spiders.leroymerlin import leroymerlinSpider
from leroymerlinparser import settings

if __name__ == '__main__':
    crawler_settings = Settings()
    crawler_settings.setmodule(settings)

    # query = input('')

    process = CrawlerProcess(settings=crawler_settings)
    process.crawl(leroymerlinSpider, search='газонокосилка')

    process.start()