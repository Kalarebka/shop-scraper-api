# Functions to interact with MongoDB
from database import db
from models import DbOffer, DbQuery

# Collections
offers = db.offers
queries = db.queries


# Manage queries


def add_query(query: str, active: bool = True) -> DbQuery:
    """Add query to the db, sets active status to True by default"""
    query = DbQuery()
    query.active = active
