import logging
from datetime import datetime

from scrapy import Request, signals
import urllib.parse as urllib
from scrapy.http import Response

from seosnap_cachewarmer.spider import SeosnapSpider

CACHE_REQUEST_FLAG = 'cache_request'


class CacheServerMiddleware(object):
    def process_request(self, request: Request, spider: SeosnapSpider):
        state = spider.state

        parsed_url = urllib.urlparse(request.url)

        if CACHE_REQUEST_FLAG not in request.meta \
                and request.url not in state.sitemap_urls() \
                and not request.url.endswith('.xml') \
                and state.cacheserver_url:
            request.meta[CACHE_REQUEST_FLAG] = True

            # Quote the request params as required by rendertron
            url = request.url

            # Add mobile param if we are rendering mobile pages
            params = {}
            if state.recache: params['refreshCache'] = 'true'

            if 'mobile' in urllib.parse_qs(parsed_url.query) and urllib.parse_qs(parsed_url.query)['mobile']:
                params['mobile'] = 1
                new_url = urllib.urlparse(url)
                query = urllib.parse_qs(new_url.query)
                query.pop('mobile', None)
                new_url = new_url._replace(query=urllib.urlencode(query, True))
                url = new_url.geturl()

            url = urllib.quote(url, safe='/:')

            return request.replace(
                url=f'{state.cacheserver_url}/{url}?{urllib.urlencode(params)}',
                method='GET' if state.recache else 'GET'
            )
        return None


class ErrorMiddleware:
    def process_response(self, request, response: Response, spider: SeosnapSpider):
        if int(response.status // 100) == 2 or int(response.status // 100) == 3:
            return response

        logging.error(f'Request to {response.url} failed with code {response.status}')
        spider.state.append_error({'url': response.url, 'time': datetime.now(), 'code': response.status})

        return response

    def process_exception(self, request, exception, spider):
        pass
