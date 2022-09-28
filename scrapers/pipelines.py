# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


import pymongo

from scrapy.conf import settings
from scrapy.exceptions import DropItem
from scrapy import log


class MongoDBPipeline:
    def __init__(self):
        client = pymongo.MongoClient(settings['MONGODB_URL'])
        db = client[settings['MONGODB_DB']]
        self.collection = db[settings['MONGODB_COLLECTION']]


    def process_item(self, item, spider):
        valid = True
        for field in item:
            if not field:
                valid = False
                raise DropItem(f"Item missing field {field}")
        if valid:
            self.collection.insert(dict(item))
            log.msg("Item added to MongoDB", level=log.DEBUG, spider=spider)
        return item

