from datetime import datetime
from typing import Iterator

import scrapy
from scrapers.items import Offer
from scrapers.base_spider import BaseSpider
from scrapy.http import TextResponse


class MatrasSpider(BaseSpider):
    name = "matras"
    allowed_domains = ["matras.pl"]
    main_url = "http://matras.pl/"

    def start_requests(self) -> Iterator[scrapy.Request]:
        for query in self.queries:
            url: str = f"{self.main_url}wyszukiwanie?szukaj={query}"
            yield scrapy.Request(
                url=url,
                callback=self.parse_search,
                meta={"query": query},
            )

    def parse_search(self, response: TextResponse) -> Iterator[scrapy.Request]:
        search_results = response.css("div.book")[:3]
        for result in search_results:
            url = result.css("div.image a.show::attr(href)").get()
            yield scrapy.Request(
                url=url,
                callback=self.parse_result,
                meta={"query": response.meta["query"]},
            )

    def parse_result(self, response: TextResponse) -> None:
        offer: Offer = Offer()
        offer["title"] = response.css(
            "div.mainContainer div#wob-link::attr(data-title)"
        ).get()
        offer["author"] = response.css("div#wob-link::attr(data-authors)").get()
        offer["timestamp"] = datetime.now()
        offer["shop"] = "matras.pl"
        offer["price"] = float(
            response.css("div.buy-schema::attr(data-price-current)").get()
        )
        offer["url"] = response.request.url

        offer["query"] = response.meta["query"]

        isbn_search = response.css("div.colsInfo").re(r"ISBN: ([\d-]+)")
        if isbn_search:
            offer["isbn"] = isbn_search[0]
        else:
            offer["isbn"] = None

        availability = (
            response.css("div.buy-schema link::attr(href)").get().split("/")[-1]
        )
        offer["available"] = availability == "InStock"

        self.db_handler.save_item_to_db(offer)
