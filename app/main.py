from fastapi import FastAPI
from . import database as db

app = FastAPI()


@app.get("/")
async def index():
    return {"app status": "working"}


@app.get("/product")
async def get_product():
    """Parameter: query (str)
    Optional: shop id, literal results only=False, max number of results, sorted by, available_only
    Returns an array of results
    Checks if there are recent (last 24 hours) results in db"""
    pass


@app.get("/history")
async def get_history():
    """Parameter: query
    Optional: from date, to date
    Returns all offers for the product sorted by date"""
    pass


@app.post("/scrape-product")
async def scrape_product():
    """Scrape the product and save results to db"""
    pass


@app.post("/batch-scrape-products")
async def batch_scrape():
    """Take a list of queries, scrape and save to db"""
    pass


@app.delete("/delete")
async def delete_query():

    pass
