import pymongo

from typing import List

from scrapers import settings
from scrapers.items import Offer
from scrapy.exceptions import DropItem


class DBHandler:
    def __init__(self):
        self.client: pymongo.MongoClient = pymongo.MongoClient(settings.MONGODB_URL)
        self.db = self.client[settings.MONGODB_DB]
        
    def save_item_to_db(self, item: Offer):
        offers_collection = self.db.offers
        valid = True
        for field in item:
            if not field:
                valid = False
                raise DropItem(f"Item missing field {field}")
        if valid:
            offers_collection.insert_one(dict(item))
        return item

    def get_queries_from_db(self) -> List[str]:
        queries_collection = self.db.queries
        query_documents = queries_collection.find({"active": True})
        queries = [query['query'] for query in query_documents]
        return queries


