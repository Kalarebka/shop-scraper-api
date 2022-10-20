from datetime import datetime
from typing import Iterator

import scrapy
from scrapers.items import Offer
from scrapers.base_spider import BaseSpider
from scrapy.http import TextResponse


class TantisSpider(BaseSpider):
    name = "tantis"
    allowed_domains = ["tantis.pl"]
    main_url = "http://tantis.pl/"

    def start_requests(self) -> Iterator[scrapy.Request]:
        for query in self.queries:
            url: str = f"{self.main_url}szukaj?query={query}"
            yield scrapy.Request(
                url=url,
                callback=self.parse_search,
                meta={"query": query},
            )

    def parse_search(self, response: TextResponse) -> Iterator[scrapy.Request]:
        search_results = response.css("div.product-card")[:3]
        for result in search_results:
            url = result.css("h3.product-name a::attr(href)").get()
            yield scrapy.Request(
                url=f"{self.main_url}{url}",
                callback=self.parse_result,
                meta={"query": response.meta["query"]},
            )

    def parse_result(self, response: TextResponse) -> None:
        offer = Offer()
        offer["title"] = response.css("h1.product-name::text").get()

        authors = response.css("p.product-authors a::text").getall()
        offer["author"] = ", ".join(authors)

        offer["timestamp"] = datetime.now()
        offer["shop"] = "tantis.pl"

        price = response.css("div.card-prices p.price::text").re(r"\d\d,\d\d")
        offer["price"] = float(price[0].replace(",", "."))

        offer["url"] = response.request.url
        offer["query"] = response.meta["query"]

        offer["isbn"] = None

        availability = response.css("span.product-estimated-delivery::text").get()
        offer["available"] = availability != "Niedostępny"

        self.db_handler.save_item_to_db(offer)
