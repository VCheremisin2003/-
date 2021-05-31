import scrapy
from scrapy.http import HtmlResponse
from bookparser.items import Books24Item


class Book24ruSpider(scrapy.Spider):
    name = 'book24'
    allowed_domains = ['book24.ru']
    start_urls = ['https://book24.ru/search/?q=шекспир']




    def parse(self, response : HtmlResponse, page=2):
        next_page = 'https://book24.ru/search/page-' + str(page) + '/?q=шекспир'
        page += 1
        try:
            response.xpath("//div[contains(text(), 'По запросу')]")
        except:
            pass

        yield response.follow(next_page, callback=self.parse)

        books_links = response.xpath("//a[@itemprop = 'name']/@href").extract()
        for link in books_links:
            yield response.follow(link, callback= self.book_parse)

    def book_parse(self, response: HtmlResponse):
        link = response.url
        name = response.xpath("//h1[@class = 'item-detail__title']/text()").extract_first()
        author = response.xpath("//a[@itemprop = 'author']/text()").extract_first()
        price = response.xpath("//b[@itemprop = 'price']/text()").extract_first()
        rate = response.xpath("//span[@itemprop = 'ratingValue']/text()").extract_first()
        item = Books24Item(name=name, author=author, price = price, link=link, rate=rate)
        yield item