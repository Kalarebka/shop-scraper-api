from datetime import datetime
from typing import List, Union

from fastapi import APIRouter
from fastapi import Body, FastAPI, HTTPException, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse, Response

from app.models import Offer, Query, UpdateQuery
from app.scraping_requests import request_live_query


router = APIRouter(prefix="/query")


@router.get("/product")
async def get_product(query: str, no_cache: bool = False) -> List[Offer]:
    if no_cache == False:
        # TODO should search for offers from the last 24h; if there are none, send a request
        # TODO optional parameter to only return available offers?
        offers = await db["offers"].find({"query": query}).to_list(length=10)
        if offers:
            return offers
    offers = request_live_query(query)
    return offers


@router.get("/product/history/")
async def get_history(
    query: str,
    from_date: Union[datetime, None] = None,
    to_date: Union[datetime, None] = None,
) -> List[Offer]:
    # return all saved results for a query; optionally limited from- and to- dates
    pass


@router.get("/product/search/")
async def searchxxx(title: Union[str, None] = None) -> List[Offer]:
    # Search offer in database by arbitrary set of parameters
    # title, author (db regex search)
    # ISBN (if available) (convert to no "-"s both in app and in scraper)
    # availability

    pass
