import os
from datetime import datetime
from enum import Enum
from typing import List, Union

from fastapi import Body, FastAPI, HTTPException, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse, Response
from motor import motor_asyncio

from app.models import Offer, Query, UpdateQuery
from app.scraping_requests import request_live_query

app = FastAPI(debug=True)
client = motor_asyncio.AsyncIOMotorClient(os.environ["MONGODB_URL"])
db = client["shop_scraper"]


@app.get("/")
async def index() -> dict:
    return {"app status": "working"}


# Automatic queries management
class Mode(str, Enum):
    get_all = "all"
    active = "active"
    inactive = "inactive"


@app.get("/queries/{mode}", response_model=List[Query])
async def get_queries(mode: Mode, max_results: Union[int, None] = None) -> List[Query]:
    queries: List[Query]
    if mode == Mode.inactive:
        queries = (
            await db["queries"].find({"active": False}).to_list(length=max_results)
        )
    elif mode == Mode.active:
        queries = await db["queries"].find({"active": True}).to_list(length=max_results)
    else:
        queries = await db["queries"].find().to_list(length=max_results)
    return queries


@app.post("/queries/", response_model=Query)
async def add_query(query: Query = Body(...)) -> JSONResponse:
    query = jsonable_encoder(query)
    new_query = await db["queries"].insert_one(query)
    added_query = await db["queries"].find_one({"_id": new_query.inserted_id})
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=added_query)


@app.put("/queries/{id}", response_model=Query)
async def update_query(id: str, query: UpdateQuery = Body(...)) -> Query:
    query_update = {k: v for k, v in query.dict().items() if v is not None}

    if len(query_update) >= 1:
        result = await db["queries"].update_one({"_id": id}, {"$set": query_update})

        if result.modified_count == 1:
            updated_query = await db["queries"].find_one("{_id}: id")
            if updated_query is not None:
                return updated_query

    existing_query = await db["queries"].find_one({"_id": id})
    if existing_query is not None:
        return existing_query

    raise HTTPException(status_code=404, detail=f"Query {id} not found")


@app.delete("/queries/{id}")
async def delete_query(id: str) -> Response:
    result = await db["queries"].delete_one({"_id": id})

    if result.deleted_count == 1:
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    raise HTTPException(status_code=404, detail=f"Query {id} not found")


# Retrieving data from database (UNDER CONSTRUCTION)


@app.get("/product/offers")
async def get_product(query: str, no_cache: bool = False) -> List[Offer]:
    if no_cache == False:
        # TODO should search for offers from the last 24h; if there are none, send a request
        # TODO optional parameter to only return available offers?
        offers = await db["offers"].find({"query": query}).to_list(length=10)
        if offers:
            return offers
    offers = request_live_query(query)
    return offers


@app.get("/product/history/")
async def get_history(
    query: str,
    from_date: Union[datetime, None] = None,
    to_date: Union[datetime, None] = None,
) -> List[Offer]:
    # return all saved results for a query; optionally limited from- and to- dates
    pass


@app.get("/product/search/")
async def search(title: Union[str, None] = None) -> List[Offer]:
    # Search offer in database by arbitrary set of parameters
    # title, author (db regex search)
    # ISBN (if available) (convert to no "-"s both in app and in scraper)
    # availability
    pass
