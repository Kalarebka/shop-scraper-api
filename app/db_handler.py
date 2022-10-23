import os

from motor import motor_asyncio

from typing import List, Union

from .models import Offer, Query


class DBHandler:
    def __init__(self) -> None:
        self.client = motor_asyncio.AsyncIOMotorClient(os.environ["MONGODB_URL"])
        self.db = self.client[os.environ["MONGODB_DB"]]
        self.queries = self.db["queries"]
        self.offers = self.db["offers"]

    async def get_queries(
        self, filter: dict = {}, max_results: Union[int, None] = None
    ) -> List[dict]:
        queries = await self.queries.find(filter=filter).to_list(length=max_results)
        return queries

    async def create_query(self, query: dict) -> dict:
        new_query = await self.queries.insert_one(query)
        added_query = await self.queries.find_one({"_id": new_query.inserted_id})
        return added_query

    async def update_query(self, id: str, update: dict) -> Union[dict, None]:
        result = await self.queries.update_one({"_id": id}, {"$set": update})
        if result.modified_count == 1:
            updated_query = await self.get_query_by_id(id)
            return updated_query
        return None

    async def get_query_by_id(self, id: str) -> Union[dict, None]:
        query = await self.queries.find_one({"_id": id})
        return query

    async def delete_query(self, id: str) -> Union[dict, None]:
        result = await self.queries.delete_one({"_id": id})
        return result.deleted_count
