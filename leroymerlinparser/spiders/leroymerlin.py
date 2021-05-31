import scrapy
from scrapy.http import HtmlResponse
from leroymerlinparser.items import leroymerlinItem
from scrapy.loader import ItemLoader


class leroymerlinSpider(scrapy.Spider):
    name = 'leroymerlin'
    allowed_domains = ['leroymerlin.ru']

    def __init__(self, search):
        super(leroymerlinSpider, self).__init__()
        self.start_urls = [f'https://leroymerlin.ru/search/?q={search}']

    def parse(self, response: HtmlResponse):
        try:
            next = response.xpath("//a[contains(@aria-label,'Следующая')]/@href").extract_first()
        except:
            pass
        yield response.follow(next, callback=self.parse)

        goods_links = response.xpath("//a[contains(@class,'bex6mjh_plp b1f5t594_plp iypgduq_plp')]")
        for link in goods_links:
            yield response.follow(link, callback=self.parse_good)

    def parse_good(self, response: HtmlResponse):
        loader = ItemLoader(item=leroymerlinItem(), response=response)

        loader.add_xpath('name', "//h1[@slot='title']/text()")
        loader.add_xpath('photos', "//img[@slot='thumbs-tail']/@src")
        loader.add_value('link', response.url)
        loader.add_xpath('chars', "//div[@class='def-list__group']//text()")
        loader.add_xpath('price', "//span[@slot='price']/text()")

        yield loader.load_item()




