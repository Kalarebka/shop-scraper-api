from __future__ import annotations

import os
from datetime import datetime, timedelta
from typing import List, Optional, Union

from motor import motor_asyncio
from pymongo.results import DeleteResult

from .models import OfferSearch, Query


class Singleton(type):
    _instances: dict = {}

    def __call__(cls, *args, **kwargs):  # type: ignore
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class DBHandler(metaclass=Singleton):
    def __init__(self) -> None:
        self.client = motor_asyncio.AsyncIOMotorClient(os.environ["MONGODB_URL"])
        self.db = self.client[os.environ["MONGODB_DB"]]
        self.queries = self.db["queries"]
        self.offers = self.db["offers"]

    async def get_queries(
        self, find_filter: dict = {}, max_results: Union[int, None] = None
    ) -> List[dict]:
        queries: List[dict] = await self.queries.find(find_filter).to_list(
            length=max_results
        )
        return queries

    async def create_query(self, query: Query) -> str:
        new_query_id: str = await self.queries.insert_one(query).inserted_id
        return new_query_id

    async def update_query(self, id: str, update: dict) -> Optional[str]:
        result = await self.queries.update_one({"_id": id}, {"$set": update})
        if result.modified_count == 1:
            return id
        return None

    async def get_query_by_id(self, id: str) -> Optional[dict]:
        query: Optional[dict] = await self.queries.find_one({"_id": id})
        return query

    async def delete_query(self, id: str) -> int:
        result: DeleteResult = await self.queries.delete_one({"_id": id})
        return result.deleted_count

    async def get_offers(self, query: str, hours: int = 24) -> List[dict]:
        """Return results for the query from the database from the last <hours> hours"""
        now = datetime.now() - timedelta(hours=hours)
        result: List[dict] = await self.offers.find(
            {"query": query, "timestamp": {"$gt": now}}, {"_id": 0}
        ).to_list(length=None)
        return result

    async def filter_offers(self, params: OfferSearch) -> List[dict]:
        """Accept search parameters as an instance of OfferSearch class
        Return results from the database with arbitrary set of filtering parameters."""
        filter_params = params.create_filter_dict()

        results: List[dict] = (
            await self.offers.find(filter=filter_params, limit=params.max_results)
            .sort(params.sorted_by, params.sort_order)
            .to_list(length=None)
        )
        return results
