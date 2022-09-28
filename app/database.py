import pymongo
import os

client = pymongo.MongoClient(os.environ["MONGODB_URL"])
db = client["shop_scraper"]
