from typing import List

from pymongo import MongoClient
from scrapy.exceptions import DropItem

from scrapers import settings
from scrapers.items import Offer


class DBHandler:
    def __init__(self) -> None:
        self.client: MongoClient = MongoClient(settings.MONGODB_URL)
        self.db = self.client[settings.MONGODB_DB]

    def save_item_to_db(self, item: Offer) -> Offer:
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
        queries = [query["query"] for query in query_documents]
        return queries
