
import scrapy
from itemloaders.processors import MapCompose, TakeFirst

def change_url(value):
    try:
        res = value.replace('w_82', 'w_2000')
        result = res.replace('h_82', 'h_2000')
        return result
    except Exception:
        return value

def clear(value):
    try:
        result = value.replace(' ', '').replace('\n','')
    except Exception:
        return value
    return result



def price_int(value):
    result = int(value[0])
    return result

class leroymerlinItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field(output_processor=TakeFirst())
    photos = scrapy.Field(input_processor=MapCompose(change_url))
    link = scrapy.Field()
    chars = scrapy.Field(input_processor=MapCompose(clear))
    price = scrapy.Field(output_processor=MapCompose(price_int))

