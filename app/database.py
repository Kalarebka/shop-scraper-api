import pymongo
import os

client: pymongo.MongoClient = pymongo.MongoClient(os.environ["MONGODB_URL"])
db = client["shop_scraper"]
