# under construction

from scrapy import spiderloader

from scrapy.crawler import Crawler, CrawlerProcess
from scrapy.settings import Settings
from scrapy.utils.project import get_project_settings


def run_spiders(query: str = None) -> None:
    # This is one big TODO at the moment
    settings: Settings = get_project_settings()

    # ? Would it be faster to hard-code the spider classes?
    spider_loader = spiderloader.SpiderLoader.from_settings(settings)
    spiders = spider_loader.list()

    process = CrawlerProcess(settings)

    for spider in spiders:
        crawler = Crawler(
            spider,
            settings={
                **settings,
            },
        )
        process.crawl(crawler, query=query)

    process.start()
