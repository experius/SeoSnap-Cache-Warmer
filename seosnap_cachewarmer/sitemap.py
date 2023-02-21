from scrapy.http import Response
from scrapy.spiders import SitemapSpider
from seosnap_cachewarmer.state import SeosnapState
import itertools
from scrapy.http import Request, XmlResponse

class SeoSnapSitemapRefresher(SitemapSpider):
    name = 'test'
    state: SeosnapState

    def __init__(self, *args, **kwargs) -> None:
        self.state = SeosnapState(*args, **kwargs)
        super().__init__(sitemap_urls=self.state.sitemap_urls())

    def parse(self, response):
        yield response

    def get_urls(self):
        for url in self.state.sitemap_urls():
            yield Request(url, self.parse)
