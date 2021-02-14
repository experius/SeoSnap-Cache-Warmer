from scrapy import Request, signals

from seosnap_cachewarmer.spider import SeosnapSpider

CACHE_REQUEST_FLAG = 'cache_request'


class CacheServerMiddleware(object):
    def process_request(self, request: Request, spider: SeosnapSpider):
        state = spider.state

        if CACHE_REQUEST_FLAG not in request.meta \
                and request.url not in state.sitemap_urls() \
                and not request.url.endswith('.xml') \
                and state.cacheserver_url:
            request.meta[CACHE_REQUEST_FLAG] = True
            return request.replace(
                url=f'{state.cacheserver_url}/{request.url}',
                method='PUT' if state.recache else 'GET'
            )
        return None
