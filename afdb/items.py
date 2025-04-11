# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from itemloaders.processors import TakeFirst


class AfdbItem(scrapy.Item):
    url = scrapy.Field(output_processor=TakeFirst())
    title = scrapy.Field(output_processor=TakeFirst())
    brand = scrapy.Field(output_processor=TakeFirst())
    description = scrapy.Field(output_processor=TakeFirst())
    category = scrapy.Field(output_processor=TakeFirst())
    image_urls = scrapy.Field(output_processor=TakeFirst())
    sku = scrapy.Field(output_processor=TakeFirst())
    type = scrapy.Field(output_processor=TakeFirst())
    finition = scrapy.Field(output_processor=TakeFirst())
    stock = scrapy.Field(output_processor=TakeFirst())
    details = scrapy.Field(output_processor=TakeFirst())
    variure = scrapy.Field(output_processor=TakeFirst())


