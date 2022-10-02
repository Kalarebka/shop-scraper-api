from scrapy import CrawlerProcess
from spiders.matras import MatrasSpider


# This is one big TODO at the moment
process = CrawlerProcess()
process.crawl(MatrasSpider, live_query="query")
# "Returns a deferred that is fired when the crawling is finished."
