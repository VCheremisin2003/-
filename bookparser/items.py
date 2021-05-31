# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class LabirintItem(scrapy.Item):
    name = scrapy.Field()
    author = scrapy.Field()
    publisher = scrapy.Field()
    new_price = scrapy.Field()
    old_price = scrapy.Field()
    link = scrapy.Field()
    rate = scrapy.Field()
    _id = scrapy.Field()

class Books24Item(scrapy.Item):
    name = scrapy.Field()
    author = scrapy.Field()
    price = scrapy.Field()
    link = scrapy.Field()
    rate = scrapy.Field()
    _id = scrapy.Field()

