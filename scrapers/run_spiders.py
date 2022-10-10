# under construction

from scrapy import spiderloader

from scrapy.crawler import CrawlerRunner
from scrapy.settings import Settings
from scrapy.utils.project import get_project_settings

from twisted.internet import reactor, defer


def run_spiders(query: str = None) -> None:
    # This is one big TODO at the moment
    settings: Settings = get_project_settings()

    # ? Would it be faster to hard-code the spider classes?
    spider_loader = spiderloader.SpiderLoader.from_settings(settings)
    spiders = spider_loader.list()

    runner = CrawlerRunner(settings)
    deferreds = set()

    for spider in spiders:
        d = runner.crawl(spider)
        deferreds.add(d)

    # Twisted reactor will be stopped after either all spiders finish running or there's an error
    defer.DeferredList(deferreds).addBoth(lambda _: reactor.stop())

    reactor.run()
