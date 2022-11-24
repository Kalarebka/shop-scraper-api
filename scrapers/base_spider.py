from typing import Any, Union

import scrapy

from scrapers.db_handler import DBHandler


class BaseSpider(scrapy.Spider):
    def __init__(
        self, query: Union[str, None] = None, *args: str, **kwargs: Any
    ) -> None:
        super(BaseSpider, self).__init__(*args, **kwargs)
        self.db_handler = DBHandler()
        if query:
            self.queries = [
                query,
            ]
        else:
            self.queries = self.db_handler.get_queries_from_db()
