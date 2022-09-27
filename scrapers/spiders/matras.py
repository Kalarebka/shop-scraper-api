import scrapy

from datetime import datetime

from scrapers.items import Offer


class MatrasSpider(scrapy.Spider):
    name = "matras"
    allowed_domains = ["matras.pl"]
    main_url = "http://matras.pl/"

    def start_requests(self):
        # with open("queries.txt", "r") as f:
        #     for line in f:
        #         if len(line) > 1:
        #             query = line.strip()
        #             queries.append(query)
        data = ["ziemiomorze,3", "kochamy plutona,3"]
        queries = [query.strip().split(",") for query in data]
        for query, num_results in queries:
            url = f"{self.main_url}wyszukiwanie?szukaj={query}&l=20"
            yield scrapy.Request(
                url=url,
                callback=self.parse_search,
                meta={"query": query, "num_results": num_results},
            )

    def parse_search(self, response):
        search_results = response.css("div.book")
        for result in search_results:
            url = result.css("div.image a.show::attr(href)").get()
            yield scrapy.Request(url=url, callback=self.parse_result)

    def parse_result(self, response):
        offer = Offer()
        offer["title"] = response.css(
            "div.mainContainer div#wob-link::attr(data-title)"
        ).get()
        offer["author"] = response.css("div#wob-link::attr(data-authors)").get()
        offer["timestamp"] = datetime.now()
        offer["shop"] = "matras.pl"
        offer["price"] = response.css("div.buy-schema::attr(data-price-current)").get()
        offer["url"] = response.request.url

        isbn_search = response.css("div.colsInfo").re(r"ISBN: ([\d-]+)")
        if isbn_search:
            offer["isbn"] = isbn_search[0]
        else:
            offer["isbn"] = None

        availability = (
            response.css("div.buy-schema link::attr(href)").get().split("/")[-1]
        )
        offer["available"] = availability == "InStock"

        yield offer
