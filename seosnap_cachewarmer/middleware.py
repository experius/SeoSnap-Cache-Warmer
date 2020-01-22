from scrapy import Request, signals

from seosnap_cachewarmer.spider import SeosnapSpider

CACHE_REQUEST_FLAG = 'cache_request'


class CacheServerMiddleware(object):
    def process_request(self, request: Request, spider: SeosnapSpider):
        if CACHE_REQUEST_FLAG not in request.meta \
                and request.url not in spider.sitemap_urls \
                and spider.cacheserver_url:
            request.meta[CACHE_REQUEST_FLAG] = True
            return request.replace(
                url=f'{spider.cacheserver_url}/{request.url}',
                method='PUT' if spider.recache else 'GET'
            )
        return None
