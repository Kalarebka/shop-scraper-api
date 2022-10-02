# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class Offer(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title: scrapy.Field = scrapy.Field()
    author: scrapy.Field = scrapy.Field()
    isbn: scrapy.Field = scrapy.Field()
    timestamp: scrapy.Field = scrapy.Field()
    shop: scrapy.Field = scrapy.Field()
    price: scrapy.Field = scrapy.Field()
    available: scrapy.Field = scrapy.Field()
    url: scrapy.Field = scrapy.Field()
    query: scrapy.Field = scrapy.Field()
