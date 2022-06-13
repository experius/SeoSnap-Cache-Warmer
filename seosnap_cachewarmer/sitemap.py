from scrapy.http import Response
from scrapy.spiders import SitemapSpider
from seosnap_cachewarmer.state import SeosnapState
import itertools
from scrapy.http import Request, XmlResponse


class SeoSnapSitemapRefresherTest(SitemapSpider):
    state: SeosnapState
    name = 'Seosnap'
    sitemap_urls = ['http://192.168.128.5/pub/sitemap/sitemap.xml']

    def __init__(self, *args, **kwargs) -> None:
        print(' -------------- sitemap init!!! ----------- ')
        self.state = SeosnapState(*args, **kwargs)
        self.name = self.state.get_name()

        print(self.state.sitemap_urls())
        for uri in self.state.sitemap_urls():
            print(uri)

        super().__init__(sitemap_urls=self.state.sitemap_urls())

    def headers(self):
        return {}

    def parse(self, response):
        print("parse")
        print("parse")
        print("parse")
        print("parse")
        print("parse")
        print(response.url)

        # yield {
        #     'url': response.url
        # }


class SeoSnapSitemapRefresher(SitemapSpider):
    name = 'test'
    state: SeosnapState

    def __init__(self, *args, **kwargs) -> None:
        print('>>>>>>----- start sitemap ------<<<<<')
        self.state = SeosnapState(*args, **kwargs)
        super().__init__(sitemap_urls=self.state.sitemap_urls())
        # self.state = state

    def parse(self, response):
        print('test')
        print(response)

        yield response

    def get_urls(self):
        print('GET get_urls')

        for url in self.state.sitemap_urls():
            yield Request(url, self.parse)
