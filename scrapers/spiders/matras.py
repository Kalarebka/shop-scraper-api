import scrapy


class MatrasSpider(scrapy.Spider):
    name = 'matras'
    allowed_domains = ['matras.pl']
    main_url = 'http://matras.pl/'

    def parse(self, response):
        pass
