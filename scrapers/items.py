# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class Offer(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()
    author = scrapy.Field()
    isbn = scrapy.Field()
    timestamp = scrapy.Field()
    shop = scrapy.Field()
    price = scrapy.Field()
    available = scrapy.Field()
    url = scrapy.Field()
    query = scrapy.Field
