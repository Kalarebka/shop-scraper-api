import scrapy

from collections.abc import Generator
from datetime import datetime

from spiders.base_spider import BaseSpider
from scrapers.items import Offer


class BonitoSpider(scrapy.Spider):
    name = "bonito"
    allowed_domains = ["bonito.pl"]
    main_url = "http://bonito.pl/"

    def start_requests(self) -> Generator[scrapy.Request, None, None]:
        for query in self.queries:
            url = f"{self.main_url}/szukaj/?szukaj=k{query}&ordering=0"
            yield scrapy.Request(
                url=url,
                callback=self.parse_search,
                meta={"query": query},
            )

    def parse_search(
        self, response: scrapy.Response
    ) -> Generator[scrapy.Request, None, None]:
        # TODO decide how many results to scrape from a search
        search_results = response.xpath("//div[contains(@id, 'result')]")
        for result in search_results:
            url = result.xpath("//a[contains(@title, 'produkt')]//@href").get()
            yield scrapy.Request(
                url=f"{self.main_url}{url}",
                callback=self.parse_result,
                meta={"query": response.meta["query"]},
            )

    def parse_result(self, response: scrapy.Response) -> None:
        offer = Offer()
        offer["title"] = response.xpath("//h1[@itemprop='name']//text()").get()

        authors = (
            response.css("div.product_container")
            .xpath(
                "//div[1]/div[2]/div[2]/div[1]/div[2]/a[contains(@href, 'autor')]//text()"
            )
            .getall()
        )
        offer["author"] = ", ".join(authors)

        offer["timestamp"] = datetime.now()
        offer["shop"] = "bonito.pl"
        offer["price"] = response.xpath("//div[@itemprop='price']//@content").get()
        offer["url"] = response.request.url

        offer["query"] = response.meta["query"]

        offer["isbn"] = response.xpath(
            "//td[text()='Numer ISBN']/following-sibling::td//text()"
        ).get()

        availability = response.xpath(
            "//span[@itemprop='availability']//@content"
        ).get()
        offer["available"] = availability == "InStock"

        self.db_handler.save_item_to_db(offer)
