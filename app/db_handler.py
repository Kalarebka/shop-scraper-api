import re
import os

from motor import motor_asyncio
from pymongo import ASCENDING, DESCENDING

from datetime import datetime, timedelta
from typing import List, Union

from .models import OfferSearch, Query


class DBHandler:
    def __init__(self) -> None:
        self.client = motor_asyncio.AsyncIOMotorClient(os.environ["MONGODB_URL"])
        self.db = self.client[os.environ["MONGODB_DB"]]
        self.queries = self.db["queries"]
        self.offers = self.db["offers"]

    async def get_queries(
        self, filter: dict = {}, max_results: Union[int, None] = None
    ) -> List[dict]:
        queries: List[dict] = await self.queries.find(filter=filter).to_list(length=max_results)
        return queries

    async def create_query(self, query: Query) -> dict:
        new_query = await self.queries.insert_one(query)
        added_query: dict = await self.queries.find_one({"_id": new_query.inserted_id})
        return added_query

    async def update_query(self, id: str, update: dict) -> Union[dict, None]:
        result = await self.queries.update_one({"_id": id}, {"$set": update})
        if result.modified_count == 1:
            updated_query = await self.get_query_by_id(id)
            return updated_query
        return None

    async def get_query_by_id(self, id: str) -> Union[dict, None]:
        query: Union[dict, None] = await self.queries.find_one({"_id": id})
        return query

    async def delete_query(self, id: str) -> Union[dict, None]:
        result = await self.queries.delete_one({"_id": id})
        return result.deleted_count

    async def get_offers(self, query: str) -> List[dict]:
        """Return results for the query from the database from the last 24 hours"""
        now = datetime.now() - timedelta(hours=24)
        result: List[dict] = await self.offers.find({"query": query, "timestamp": {"$gt": now}}).to_list(length=None)
        return result

    async def filter_offers(self, params: OfferSearch) -> List[dict]:
        """Accept search parameter as an instance of OfferSearch class
           Return results from the database with arbitrary set of filtering parameters."""
        # Create a filter dict (title regex, author regex, isbn no dashes, dates, availability)
        
        filter_params: dict = {}
        if params.title:
            title_regex = re.compile(params.title, re.IGNORECASE)
            filter_params["title"] = title_regex
        if params.author:
            author_regex = re.compile(params.author, re.IGNORECASE)
            filter_params["author"] = author_regex
        if params.isbn:
            filter_params["isbn"] = params.isbn.replace("-", "")
        if params.from_date:
            filter_params["timestamp"] = {"$gte": params.from_date}
        if params.to_date:
            filter_params["timestamp"] = {"$lte": params.to_date}
        if params.available_only:
            filter_params["available"] = params.available_only

        if params.reverse:
            sort_order = DESCENDING
        else:
            sort_order = ASCENDING

        results: List[dict] = (
            await self.offers.find(filter=filter_params, limit=params.max_results)
            .sort(params.sorted_by, sort_order)
            .to_list(length=None)
        )
        return results
