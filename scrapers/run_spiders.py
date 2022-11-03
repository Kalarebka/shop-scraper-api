# Not used at the moment, unless I figure out how to make it work with Celery

from typing import Union

from scrapy import spiderloader
from scrapy.crawler import CrawlerRunner
from scrapy.settings import Settings
from scrapy.utils.project import get_project_settings
from twisted.internet import defer, reactor

from multiprocessing import Process
from scrapy.crawler import CrawlerProcess


def run_spiders(query: Union[str, None] = None) -> None:
    settings: Settings = get_project_settings()
    spider_loader = spiderloader.SpiderLoader.from_settings(settings)
    spiders = spider_loader.list()

    runner = CrawlerRunner(settings)
    deferreds = set()

    for spider in spiders:
        d = runner.crawl(spider)
        deferreds.add(d)

    # Twisted reactor will be stopped after either all spiders finish running or there's an error
    # defer.DeferredList(deferreds).addBoth(lambda _: reactor.stop())

    # reactor.run()
