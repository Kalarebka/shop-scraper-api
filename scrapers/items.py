# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ScraperOffer(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()
    author = scrapy.Field()
    isbn = scrapy.Field()
    timestamp = scrapy.Field()
    shop_id = scrapy.Field()
    price = scrapy.Field()
    shipping = scrapy.Field()
    exact = scrapy.Field()
    available = scrapy.Field()
    url = scrapy.Field()


