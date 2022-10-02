import scrapy

from scrapers.db_handler import DBHandler


class BaseSpider(scrapy.Spider):
    def __init__(self, live_query=None, *args, **kwargs):
        super(BaseSpider, self).__init__(*args, **kwargs)
        self.db_handler = DBHandler()
        if live_query:
            self.queries = [live_query,]
        else:
            self.queries = self.db_handler.get_queries_from_db()