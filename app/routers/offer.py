from typing import List

from fastapi import APIRouter
from fastapi import Body

from app.db_handler import DBHandler
from app.live_query import request_live_query
from app.models import Offer, OfferSearch


router = APIRouter(prefix="/offer")
db = DBHandler()


@router.get("/")
async def get_offers(query: str) -> List[dict]:
    """Searches for result for the query from the last 24 hours.
    If there are none, sends a live query to the scrapers"""
    results: List[dict] = await db.get_offers(query)
    if results:
        return results
    offers = await request_live_query(query)
    return offers


@router.get("/search/", response_model=List[Offer])
async def search_offers(offer_search: OfferSearch = Body(...)) -> List[dict]:
    """Searches for results in the database with arbitrary set of parameters
    - title, author - search with regex
    - isbn, from_date, to_date
    - available_only (defaults to True)
    - sorted_by (name of the field, defaults to timestamp), reverse (defaults to True)"""
    found_offers: List[dict] = await db.filter_offers(offer_search)
    return found_offers
